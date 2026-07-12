"""主窗口：两个标签页。

  1) 迁移：选择源文件/文件夹与目标位置，移动到目标并在原位置建符号链接。
  2) 修改位置：针对已经迁移（现为符号链接）的项，把真实数据移动到新的
     存放位置，并让原符号链接重新指向新位置。
"""

import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel,
    QLineEdit, QFileDialog, QMessageBox,     QAbstractItemView, QTabWidget,
)
from PySide6.QtCore import Qt

from core import disk, symlink, migrator
from .progress_dialog import ProgressDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件迁移工具（软链接）")
        self.setMinimumWidth(640)
        self.resize(720, 520)

        self.sources = []  # 迁移页：源路径列表

        tabs = QTabWidget()
        tabs.addTab(self._build_migrate_tab(), "迁移")
        tabs.addTab(self._build_relocate_tab(), "修改位置")

        layout = QVBoxLayout(self)
        layout.addWidget(tabs)

        self._check_capability()

    # ---------------- 能力检测 ----------------
    def _check_capability(self):
        if not symlink.can_create_symlink():
            if symlink.is_admin():
                QMessageBox.warning(
                    self, "符号链接不可用",
                    "当前环境无法创建符号链接（即使是管理员）。\n"
                    "请确认系统策略允许，或启用「开发者模式」。",
                )
            else:
                ans = QMessageBox.question(
                    self, "需要管理员权限",
                    "创建符号链接需要管理员权限或「开发者模式」。\n\n"
                    "是否以管理员身份重新启动本程序？\n"
                    "（也可在 Windows 设置 → 开发者模式 中开启后继续使用。）",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )
                if ans == QMessageBox.StandardButton.Yes:
                    symlink.relaunch_as_admin()
                    import sys
                    sys.exit(0)

    # ================= 迁移页 =================
    def _build_migrate_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        tip = QLabel(
            "将选中的文件/文件夹移动到目标位置，并在原位置创建符号链接，\n"
            "使原路径上的程序与引用继续可用。保留各自名称与内部结构。"
        )
        tip.setWordWrap(True)
        layout.addWidget(tip)

        layout.addWidget(QLabel("待迁移的文件 / 文件夹："))
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        layout.addWidget(self.list_widget, stretch=1)

        src_btn_row = QHBoxLayout()
        self.btn_add_file = QPushButton("添加文件")
        self.btn_add_folder = QPushButton("添加文件夹")
        self.btn_remove = QPushButton("移除选中")
        self.btn_clear = QPushButton("清空")
        src_btn_row.addWidget(self.btn_add_file)
        src_btn_row.addWidget(self.btn_add_folder)
        src_btn_row.addWidget(self.btn_remove)
        src_btn_row.addWidget(self.btn_clear)
        src_btn_row.addStretch()
        layout.addLayout(src_btn_row)

        layout.addWidget(QLabel("目标位置（迁移目的地）："))
        dest_row = QHBoxLayout()
        self.dest_edit = QLineEdit()
        self.dest_edit.setPlaceholderText("选择目标文件夹…")
        self.btn_dest = QPushButton("选择…")
        dest_row.addWidget(self.dest_edit, stretch=1)
        dest_row.addWidget(self.btn_dest)
        layout.addLayout(dest_row)

        self.btn_start = QPushButton("开始迁移")
        self.btn_start.setMinimumHeight(40)
        self.btn_start.setStyleSheet("font-weight:bold;")
        layout.addWidget(self.btn_start)

        self.btn_add_file.clicked.connect(self._add_files)
        self.btn_add_folder.clicked.connect(self._add_folder)
        self.btn_remove.clicked.connect(self._remove_selected)
        self.btn_clear.clicked.connect(self._clear)
        self.btn_dest.clicked.connect(self._choose_dest)
        self.btn_start.clicked.connect(self._start_migrate)
        return tab

    # ---------------- 迁移页操作 ----------------
    def _add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择文件")
        for f in files:
            self._add_source(f)

    def _add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self._add_source(folder)

    def _add_source(self, path):
        absp = os.path.abspath(os.path.realpath(path))
        if absp not in self.sources:
            self.sources.append(absp)
            self.list_widget.addItem(absp)

    def _remove_selected(self):
        for item in self.list_widget.selectedItems():
            path = item.text()
            if path in self.sources:
                self.sources.remove(path)
            self.list_widget.takeItem(self.list_widget.row(item))

    def _clear(self):
        self.sources.clear()
        self.list_widget.clear()

    def _choose_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "选择目标文件夹")
        if folder:
            self.dest_edit.setText(os.path.abspath(os.path.realpath(folder)))

    def _start_migrate(self):
        if not self.sources:
            QMessageBox.information(self, "提示", "请先添加要迁移的文件或文件夹。")
            return
        dest = self.dest_edit.text().strip()
        if not dest:
            QMessageBox.information(self, "提示", "请选择目标位置。")
            return
        if not os.path.isdir(dest):
            QMessageBox.information(self, "提示", "目标位置不是一个有效文件夹。")
            return

        if disk.is_external_drive(dest):
            dtype = disk.describe_drive_type(dest)
            ans = QMessageBox.question(
                self, "目标位于外部磁盘",
                f"目标位置位于【{dtype}】，属于外部/非本地固定磁盘。\n\n"
                "在该磁盘拔出后，原位置的符号链接将无法正常访问相关文件。\n"
                "确认仍要迁移到此处吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if ans != QMessageBox.StandardButton.Yes:
                return

        total_items = len(self.sources)
        ans = QMessageBox.question(
            self, "确认迁移",
            f"即将迁移 {total_items} 个文件/文件夹到：\n{dest}\n\n"
            "操作将：移动真实数据到目标，并在原位置创建符号链接。\n"
            "确认开始？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if ans != QMessageBox.StandardButton.Yes:
            return

        srcs = self.sources[:]
        d = dest

        def task(callbacks):
            migrator.migrate(srcs, d, callbacks)

        dlg = ProgressDialog(task, total_bytes=0, title="迁移进行中", parent=self)
        dlg.show()
        dlg.start_migration()
        dlg.exec()

    # ================= 修改位置页 =================
    def _build_relocate_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        tip = QLabel(
            "针对已经迁移（现为符号链接）的项：把真实数据移动到新的存放位置，\n"
            "并让原符号链接重新指向新位置，原路径上的引用继续有效。"
        )
        tip.setWordWrap(True)
        layout.addWidget(tip)

        layout.addWidget(QLabel("已迁移项（原位置，当前为符号链接）："))
        link_row = QHBoxLayout()
        self.rel_link_edit = QLineEdit()
        self.rel_link_edit.setPlaceholderText("选择或输入符号链接路径…")
        self.btn_rel_pick_file = QPushButton("选择文件")
        self.btn_rel_pick_folder = QPushButton("选择文件夹")
        link_row.addWidget(self.rel_link_edit, stretch=1)
        link_row.addWidget(self.btn_rel_pick_file)
        link_row.addWidget(self.btn_rel_pick_folder)
        layout.addLayout(link_row)

        self.rel_current = QLabel("当前指向：—")
        self.rel_current.setWordWrap(True)
        layout.addWidget(self.rel_current)

        layout.addWidget(QLabel("新的数据存放位置："))
        dest_row = QHBoxLayout()
        self.rel_dest_edit = QLineEdit()
        self.rel_dest_edit.setPlaceholderText("选择新目标文件夹…")
        self.btn_rel_dest = QPushButton("选择…")
        dest_row.addWidget(self.rel_dest_edit, stretch=1)
        dest_row.addWidget(self.btn_rel_dest)
        layout.addLayout(dest_row)

        self.btn_rel_start = QPushButton("开始修改位置")
        self.btn_rel_start.setMinimumHeight(40)
        self.btn_rel_start.setStyleSheet("font-weight:bold;")
        layout.addWidget(self.btn_rel_start)
        layout.addStretch()

        self.rel_link_edit.textChanged.connect(self._update_rel_current)
        self.btn_rel_pick_file.clicked.connect(
            lambda: self._pick_rel_path(file=True))
        self.btn_rel_pick_folder.clicked.connect(
            lambda: self._pick_rel_path(file=False))
        self.btn_rel_dest.clicked.connect(self._choose_rel_dest)
        self.btn_rel_start.clicked.connect(self._start_relocate)
        return tab

    # ---------------- 修改位置页操作 ----------------
    def _pick_rel_path(self, file: bool):
        if file:
            p, _ = QFileDialog.getOpenFileName(self, "选择已迁移的文件（符号链接）")
        else:
            p = QFileDialog.getExistingDirectory(self, "选择已迁移的文件夹（符号链接）")
        if p:
            self.rel_link_edit.setText(os.path.abspath(os.path.realpath(p)))

    def _choose_rel_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "选择新的数据存放位置")
        if folder:
            self.rel_dest_edit.setText(os.path.abspath(os.path.realpath(folder)))

    def _update_rel_current(self, text):
        p = text.strip()
        if not p:
            self.rel_current.setText("当前指向：—")
            return
        if not os.path.islink(p):
            self.rel_current.setText("当前指向：该路径不是符号链接")
            return
        try:
            target = os.path.realpath(p)
        except OSError:
            self.rel_current.setText("当前指向：无法解析")
            return
        exists = "（目标存在）" if os.path.exists(target) else "（目标不存在！）"
        self.rel_current.setText(f"当前指向：{target} {exists}")

    def _start_relocate(self):
        link = self.rel_link_edit.text().strip()
        dest = self.rel_dest_edit.text().strip()
        if not link:
            QMessageBox.information(self, "提示", "请选择已迁移项（符号链接路径）。")
            return
        if not os.path.islink(link):
            QMessageBox.information(self, "提示", "该路径不是符号链接，无法修改其指向。")
            return
        if not dest:
            QMessageBox.information(self, "提示", "请选择新的数据存放位置。")
            return
        if not os.path.isdir(dest):
            QMessageBox.information(self, "提示", "新的数据存放位置不是有效文件夹。")
            return

        current_target = os.path.realpath(link)
        if not os.path.exists(current_target):
            QMessageBox.warning(
                self, "提示",
                f"该符号链接当前指向的目标不存在：\n{current_target}\n无法继续。")
            return

        if disk.is_external_drive(dest):
            dtype = disk.describe_drive_type(dest)
            ans = QMessageBox.question(
                self, "目标位于外部磁盘",
                f"新的数据存放位置位于【{dtype}】，属于外部/非本地固定磁盘。\n"
                "在该磁盘拔出后，原位置的符号链接将无法正常访问相关文件。\n"
                "确认仍要移动到此处吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if ans != QMessageBox.StandardButton.Yes:
                return

        ans = QMessageBox.question(
            self, "确认修改位置",
            f"将把真实数据从：\n{current_target}\n移动到：\n{dest}\n\n"
            f"之后符号链接「{link}」将指向新位置。确认开始？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if ans != QMessageBox.StandardButton.Yes:
            return

        def task(callbacks):
            migrator.relocate(link, dest, callbacks)

        dlg = ProgressDialog(task, total_bytes=0, title="修改位置进行中", parent=self)
        dlg.show()
        dlg.start_migration()
        dlg.exec()
        self._update_rel_current(link)

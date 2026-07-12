"""入口：启动文件迁移工具（软链接）。"""

import ctypes
import os
import sys
import tempfile
import traceback

from ui.qt_compat import QApplication, QIcon, QMessageBox

from core import symlink


def _resource(rel: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


def _crash_log(text: str) -> None:
    try:
        path = os.path.join(tempfile.gettempdir(), "LinkShift_crash.log")
        with open(path, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception:
        pass


def _fatal(title: str, text: str) -> None:
    _crash_log(text)
    try:
        ctypes.windll.user32.MessageBoxW(0, text, title, 0x10)
    except Exception:
        pass
    sys.exit(1)


def _check_admin_before_gui(app: QApplication) -> bool:
    """在显示 GUI 前检查符号链接能力，必要时提示提权。
    返回 True 表示继续启动 GUI，False 表示已请求提权并应退出当前进程。
    """
    if symlink.can_create_symlink():
        return True
    if symlink.is_admin():
        # 已是管理员但仍无法创建，仅警告
        QMessageBox.warning(
            None, "符号链接不可用",
            "当前环境无法创建符号链接（即使是管理员）。\n"
            "请确认系统策略允许，或启用「开发者模式」。\n\n"
            "程序仍可启动，但迁移功能将无法使用。"
        )
        return True
    # 非管理员且无权限，询问是否提权重启
    ans = QMessageBox.question(
        None, "需要管理员权限",
        "创建符号链接需要管理员权限或「开发者模式」。\n\n"
        "是否以管理员身份重新启动本程序？\n"
        "（也可在 Windows 设置 → 开发者模式 中开启后继续使用。）\n\n"
        "选择「否」将以普通权限启动，迁移功能不可用。",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    if ans == QMessageBox.StandardButton.Yes:
        if symlink.relaunch_as_admin():
            return False  # 已请求提权，退出当前进程
    return True  # 用户拒绝提权，继续以普通权限启动


def main():
    try:
        app = QApplication(sys.argv)
    except Exception:
        _fatal(
            "文件迁移工具 - 启动失败",
            "无法初始化 Qt 界面库（可能是系统缺少必要的运行库或显示驱动）。\n\n"
            "详细错误已写入：%s\\LinkShift_crash.log" % tempfile.gettempdir(),
        )
        return

    app.setApplicationName("文件迁移工具")
    try:
        app.setWindowIcon(QIcon(_resource("app_icon.ico")))
    except Exception:
        pass

    # 先检查权限，再决定是否显示主窗口
    if not _check_admin_before_gui(app):
        return  # 已请求管理员重启，退出当前进程

    try:
        from ui import MainWindow
        window = MainWindow()
        window.setWindowIcon(QIcon(_resource("app_icon.ico")))
        window.show()
        sys.exit(app.exec())
    except Exception:
        _crash_log(traceback.format_exc())
        _fatal(
            "文件迁移工具 - 启动失败",
            "主窗口初始化时发生错误：\n\n%s\n\n详细错误已写入：%s\\LinkShift_crash.log"
            % (traceback.format_exc()[-1500:], tempfile.gettempdir()),
        )


if __name__ == "__main__":
    main()

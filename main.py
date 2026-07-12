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


def _ensure_admin_or_quit() -> bool:
    """Windows 上非管理员时弹窗询问提权。
    返回 False 表示已处理（提权重启或直接退出），调用方应退出进程。
    返回 True 表示可以继续启动 GUI（已是管理员或非 Windows）。
    """
    if sys.platform != "win32":
        return True
    if symlink.is_admin():
        return True
    ans = QMessageBox.question(
        None, "需要管理员权限",
        "创建符号链接需要管理员权限。\n\n"
        "是否以管理员模式重新启动？",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    if ans == QMessageBox.StandardButton.Yes:
        if symlink.relaunch_as_admin():
            pass  # 当前进程应退出
    sys.exit(0)  # 用户选「否」或提权失败 → 直接退出


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

    # Windows 上非管理员时询问提权，否则退出
    if not _ensure_admin_or_quit():
        return

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

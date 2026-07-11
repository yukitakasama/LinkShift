"""入口：启动文件迁移工具（软链接）。"""

import os
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from ui import MainWindow


def _resource(rel: str) -> str:
    """获取资源路径（打包后为 _MEIPASS 内的路径）。"""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("文件迁移工具")
    app.setWindowIcon(QIcon(_resource("app_icon.ico")))
    window = MainWindow()
    window.setWindowIcon(QIcon(_resource("app_icon.ico")))
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

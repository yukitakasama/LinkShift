"""Qt 工具包兼容层。

优先使用 PySide6（64 位构建），不可用时回退到 PyQt5（32 位构建）。
UI 代码统一从这里导入，无需关心底层工具包。

对少量枚举差异做打补丁，使按 PySide6 风格书写的 UI 代码在 PyQt5 下也能运行：
  - QMessageBox.StandardButton.Yes / No
  - QAbstractItemView.SelectionMode.ExtendedSelection
  - Qt.AlignmentFlag.AlignBottom / AlignLeft
"""

TOOLKIT = None

if TOOLKIT is None:
    try:
        from PySide6.QtCore import QThread, QObject, Qt, Signal
        from PySide6.QtWidgets import (
            QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
            QListWidget, QLabel, QLineEdit, QFileDialog, QMessageBox,
            QAbstractItemView, QTabWidget, QDialog, QProgressBar, QTextEdit,
            QTableWidget, QTableWidgetItem, QHeaderView,
        )
        from PySide6.QtGui import QIcon, QPainter, QPen, QColor
        TOOLKIT = "PySide6"
    except ImportError:
        pass

if TOOLKIT is None:
    from PyQt5.QtCore import QThread, QObject, Qt, pyqtSignal as Signal
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
        QListWidget, QLabel, QLineEdit, QFileDialog, QMessageBox,
        QAbstractItemView, QTabWidget, QDialog, QProgressBar, QTextEdit,
        QTableWidget, QTableWidgetItem, QHeaderView,
    )
    from PyQt5.QtGui import QIcon, QPainter, QPen, QColor
    TOOLKIT = "PyQt5"


def _patch_enum(enum_cls, mapping):
    for name, val in mapping.items():
        if not hasattr(enum_cls, name):
            try:
                setattr(enum_cls, name, val)
            except Exception:
                pass


if not hasattr(QMessageBox.StandardButton, "Yes"):
    _patch_enum(QMessageBox.StandardButton,
                {"Yes": QMessageBox.Yes, "No": QMessageBox.No})

if not hasattr(QAbstractItemView.SelectionMode, "ExtendedSelection"):
    _patch_enum(QAbstractItemView.SelectionMode,
                {"ExtendedSelection": QAbstractItemView.ExtendedSelection})

if not hasattr(Qt.AlignmentFlag, "AlignBottom"):
    _patch_enum(Qt.AlignmentFlag,
                {"AlignBottom": Qt.AlignBottom, "AlignLeft": Qt.AlignLeft})

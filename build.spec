# PyInstaller 打包配置
# 用法：pyinstaller build.spec
import importlib
import sys

datas = [("app_icon.ico", ".")]
binaries = []

# 根据当前环境中可用的工具包选择 hiddenimports：
#   64 位 Windows / Linux（PySide6）或 32 位 Windows（PyQt5）。
# UI 通过 ui/qt_compat 自动适配。
_hidden = []
try:
    importlib.import_module("PySide6")
    _hidden = ["PySide6.QtCore", "PySide6.QtWidgets", "PySide6.QtGui"]
except ImportError:
    _hidden = ["PyQt5.QtCore", "PyQt5.QtWidgets", "PyQt5.QtGui"]

hiddenimports = _hidden

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# Windows 下产物名为中文（与历史一致）；Linux 下用 ASCII 名便于分发。
_exe_name = "文件迁移工具" if sys.platform == "win32" else "LinkShift"

_exe_kwargs = dict(
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
# 图标仅 Windows 支持 .ico
if sys.platform == "win32":
    _exe_kwargs["icon"] = "app_icon.ico"

exe = EXE(
    pyz,
    a.binaries,
    a.datas,
    [],
    name=_exe_name,
    **_exe_kwargs,
)

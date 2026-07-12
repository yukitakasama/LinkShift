# PyInstaller 打包配置
# 用法：pyinstaller build.spec
import importlib

datas = [("app_icon.ico", ".")]
binaries = []

# 根据当前环境中可用的工具包选择 hiddenimports：
#   64 位（PySide6）或 32 位（PyQt5）。UI 通过 ui/qt_compat 自动适配。
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

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.binaries,
    a.datas,
    [],
    name="文件迁移工具",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # 不显示控制台窗口
    icon="app_icon.ico",    # exe 文件图标
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

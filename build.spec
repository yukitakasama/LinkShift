# PyInstaller 打包配置
# 用法：pyinstaller build.spec
from PyInstaller.utils.hooks import collect_all

datas = [("app_icon.ico", ".")]
binaries = []
hiddenimports = [
    "PySide6.QtCharts",
    "PySide6.QtCore",
    "PySide6.QtWidgets",
    "PySide6.QtGui",
]

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
    a.scripts,
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

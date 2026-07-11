"""外部/网络磁盘检测。

通过 Windows API GetDriveTypeW 判断目标路径所在盘符的类型。
DriveType 取值（部分）：
  0  未知
  2  可移动磁盘（U 盘等外接盘）
  3  固定本地磁盘
  4  网络映射盘
  5  CD-ROM
除 3（固定本地磁盘）之外，都视为「非本地固定盘」，需要提醒用户。
"""

import os
import ctypes
from ctypes import wintypes

_kernel32 = ctypes.windll.kernel32

_DRIVE_TYPE_NAMES = {
    0: "未知",
    1: "不存在",
    2: "可移动磁盘",
    3: "本地固定磁盘",
    4: "网络磁盘",
    5: "CD-ROM",
    6: "RAM 磁盘",
}


def _drive_of(path: str) -> str | None:
    """返回路径所在盘符（如 'C:'），无法判断时返回 None。"""
    try:
        abspath = os.path.abspath(os.path.realpath(path))
    except Exception:
        return None
    if len(abspath) >= 2 and abspath[1] == ":":
        return abspath[:2].upper()
    # UNC 路径
    if abspath.startswith("\\\\"):
        return abspath
    return None


def get_drive_type(path: str) -> int:
    """返回路径所在盘符的 DriveType 整数值。"""
    drive = _drive_of(path)
    if not drive:
        return 0
    # GetDriveTypeW 接受带反斜杠的盘符如 "C:\\" 或 UNC
    if len(drive) == 2:
        arg = drive + "\\"
    else:
        arg = drive
    try:
        return _kernel32.GetDriveTypeW(arg)
    except Exception:
        return 0


def is_external_drive(path: str) -> bool:
    """目标路径是否位于非本地固定磁盘（外接盘 / 网络盘等）。"""
    return get_drive_type(path) != 3


def describe_drive_type(path: str) -> str:
    return _DRIVE_TYPE_NAMES.get(get_drive_type(path), "未知")

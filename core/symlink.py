"""符号链接创建与能力检测 / 提权。

Windows 下创建符号链接默认需要管理员权限，或在「开发者模式」下关闭该限制。
本模块负责：
  - 检测当前进程是否具备创建符号链接的能力（试建测试链接）；
  - 若不具备，提供以管理员身份重新启动本程序的入口。
"""

import ctypes
import os
import sys
import tempfile
from ctypes import wintypes

# DriveType / symlink 相关常量
SYMBOLIC_LINK_FLAG_DIRECTORY = 0x1
SYMBOLIC_LINK_FLAG_ALLOW_UNPRIVILEGED_CREATE = 0x2


def can_create_symlink() -> bool:
    """尝试在临时目录创建一个测试符号链接，判断当前进程是否具备能力。"""
    try:
        tmp = tempfile.gettempdir()
        target = os.path.join(tmp, "symlink_test_target")
        link = os.path.join(tmp, "symlink_test_link")
        with open(target, "w") as f:
            f.write("t")
        if os.path.islink(link) or os.path.exists(link):
            try:
                os.remove(link)
            except OSError:
                pass
            try:
                os.remove(target)
            except OSError:
                pass
            # 已存在可能是上次残留，仍可创建则视为 ok；这里直接重试
        try:
            os.symlink(target, link)
            ok = os.path.islink(link)
            try:
                os.remove(link)
            except OSError:
                pass
            try:
                os.remove(target)
            except OSError:
                pass
            return ok
        except OSError:
            try:
                os.remove(target)
            except OSError:
                pass
            return False
    except Exception:
        return False


def is_admin() -> bool:
    """判断当前进程是否具备创建符号链接所需权限。

    Windows 下需要管理员或「开发者模式」；Linux/Posix 普通用户即可创建，
    因此非 Windows 一律返回 True（视为具备能力）。
    """
    if sys.platform != "win32":
        return True
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin() -> None:
    """以管理员身份重新启动当前 Python 程序（仅 Windows 有效）。"""
    if sys.platform != "win32":
        return  # 非 Windows 无此需求
    args = " ".join(f'"{a}"' for a in sys.argv)
    exe = sys.executable
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", exe, args, None, 1
    )


def create_symlink(target: str, link: str, target_is_directory: bool = False) -> None:
    """创建符号链接 link -> target。

    优先使用 os.symlink；失败时回退到 CreateSymbolicLinkW（带允许非特权创建标志）。
    任何失败都会抛出 OSError；调用方应以 verify_symlink 再次确认链接有效。
    """
    if os.path.islink(link) or os.path.exists(link):
        raise FileExistsError(f"链接路径已存在：{link}")

    try:
        os.symlink(target, link, target_is_directory=target_is_directory)
        return
    except (OSError, NotImplementedError):
        pass

    if sys.platform != "win32":
        # 非 Windows 下 os.symlink 即应成功；失败直接抛出
        raise OSError(f"无法创建符号链接：{link} -> {target}")

    # 回退到 Win32 API
    _kernel32 = ctypes.windll.kernel32
    flag = SYMBOLIC_LINK_FLAG_ALLOW_UNPRIVILEGED_CREATE
    if target_is_directory:
        flag |= SYMBOLIC_LINK_FLAG_DIRECTORY
    target_w = ctypes.c_wchar_p(target)
    link_w = ctypes.c_wchar_p(link)
    ret = _kernel32.CreateSymbolicLinkW(link_w, target_w, wintypes.DWORD(flag))
    if not ret:
        err = ctypes.GetLastError()
        raise OSError(err, f"CreateSymbolicLinkW 失败 (code {err})")


def verify_symlink(link: str, target_is_directory: bool = False) -> bool:
    """确认 link 是一个指向有效目标的符号链接。"""
    if not os.path.islink(link):
        return False
    try:
        if target_is_directory:
            return os.path.isdir(link)
        return os.path.exists(link)
    except OSError:
        return False

"""外部/网络磁盘检测（跨平台）。

Windows：通过 GetDriveTypeW 判断路径所在盘符的类型。
Linux/Posix：通过 /proc/self/mountinfo 找出路径所在挂载点的文件系统类型，
             判断是否为可移动/网络等非本地固定磁盘。
"""

import os
import sys

# ================= Windows 实现 =================
if sys.platform == "win32":
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

    def _drive_of(path: str):
        """返回路径所在盘符（如 'C:'），无法判断时返回 None。"""
        try:
            abspath = os.path.abspath(os.path.realpath(path))
        except Exception:
            return None
        if len(abspath) >= 2 and abspath[1] == ":":
            return abspath[:2].upper()
        if abspath.startswith("\\\\"):
            return abspath
        return None

    def get_drive_type(path: str) -> int:
        """返回路径所在盘符的 DriveType 整数值。"""
        drive = _drive_of(path)
        if not drive:
            return 0
        arg = drive + "\\" if len(drive) == 2 else drive
        try:
            return _kernel32.GetDriveTypeW(arg)
        except Exception:
            return 0

    def is_external_drive(path: str) -> bool:
        """目标路径是否位于非本地固定磁盘（外接盘 / 网络盘等）。"""
        return get_drive_type(path) != 3

    def describe_drive_type(path: str) -> str:
        return _DRIVE_TYPE_NAMES.get(get_drive_type(path), "未知")

# ================= Linux / Posix 实现 =================
else:
    # 视为「外部 / 网络」的文件系统类型
    _EXTERNAL_FSTYPES = {
        "vfat", "exfat", "ntfs", "msdos", "udf", "iso9660",
        "nfs", "nfs4", "cifs", "smb3", "smbfs", "fuseblk",
        "fusefs", "davfs", "sshfs", "mtpfs", "gphotofs",
    }

    _TYPE_NAMES = {
        "vfat": "FAT 可移动磁盘",
        "exfat": "exFAT 可移动磁盘",
        "ntfs": "NTFS 外接磁盘",
        "msdos": "DOS 可移动磁盘",
        "udf": "UDF 光盘",
        "iso9660": "ISO 光盘",
        "nfs": "NFS 网络磁盘",
        "nfs4": "NFS 网络磁盘",
        "cifs": "SMB/CIFS 网络磁盘",
        "smb3": "SMB 网络磁盘",
        "smbfs": "SMB 网络磁盘",
        "fuseblk": "FUSE 外接磁盘",
        "fusefs": "FUSE 外接磁盘",
        "davfs": "WebDAV 网络磁盘",
        "sshfs": "SSHFS 网络磁盘",
        "mtpfs": "MTP 设备",
        "gphotofs": "相机设备",
    }

    def _safe_abspath(path: str):
        try:
            return os.path.abspath(os.path.realpath(path))
        except Exception:
            return ""

    def _mount_info(path):
        """返回 (挂载点, 文件系统类型)，无法判定时返回 (None, None)。"""
        ap = _safe_abspath(path)
        if not ap:
            return None, None
        best_mount = None
        best_fs = None
        try:
            with open("/proc/self/mountinfo", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.split()
                    # 格式：... <root> <mountpoint> - <fstype> <source> <opts>
                    try:
                        idx = parts.index("-")
                    except ValueError:
                        continue
                    if idx + 1 >= len(parts):
                        continue
                    fstype = parts[idx + 1]
                    mountpoint = parts[idx - 1]
                    if ap == mountpoint or ap.startswith(mountpoint + os.sep):
                        if best_mount is None or len(mountpoint) > len(best_mount):
                            best_mount = mountpoint
                            best_fs = fstype
        except OSError:
            return None, None
        return best_mount, best_fs

    def get_drive_type(path: str) -> int:
        """兼容占位：Linux 下无整数 DriveType 概念，这里借用语义。"""
        _, fs = _mount_info(path)
        if fs is None:
            return 0
        return 2 if fs in _EXTERNAL_FSTYPES else 3

    def is_external_drive(path: str) -> bool:
        """目标路径是否位于可移动/网络等非本地固定磁盘。"""
        mp, fs = _mount_info(path)
        if fs is not None and fs in _EXTERNAL_FSTYPES:
            return True
        check = mp if mp else _safe_abspath(path)
        if check and (check.startswith("/media/") or check.startswith("/mnt/")):
            return True
        return False

    def describe_drive_type(path: str) -> str:
        _, fs = _mount_info(path)
        if fs is None:
            return "未知"
        return _TYPE_NAMES.get(fs, f"{fs} 文件系统")

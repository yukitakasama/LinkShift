"""迁移主逻辑。

把选中的源文件/文件夹真正移动到目标位置（保留各自名称与内部结构），
然后在原位置创建符号链接指向新位置。

进度通过回调向外回报：
    on_progress(done_bytes, total_bytes)
    on_speed(bytes_per_sec, elapsed_sec)
    on_item_start(name)
    on_log(message)
    on_finished(success_count, error_count)
    on_error(message)
"""

import os
import shutil
import time

from . import symlink as symlink_mod
from . import disk as disk_mod

CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB 分块复制，便于统计速度与进度


class Cancelled(Exception):
    """迁移/修改过程中被用户取消。"""


def _iter_files(src: str):
    """递归产出源目录下所有文件路径（相对目录根）。"""
    for root, _dirs, files in os.walk(src):
        for name in files:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, src)
            yield rel


def total_size(path: str) -> int:
    """统计文件或文件夹的总字节数。"""
    if os.path.isfile(path):
        try:
            return os.path.getsize(path)
        except OSError:
            return 0
    total = 0
    for root, _dirs, files in os.walk(path):
        for name in files:
            fp = os.path.join(root, name)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total


def _unique_dest(dest_dir: str, name: str) -> str:
    """在目标目录中生成不冲突的目标路径（同名则追加 (1) (2)...）。"""
    base, ext = os.path.splitext(name)
    candidate = os.path.join(dest_dir, name)
    i = 1
    while os.path.exists(candidate):
        candidate = os.path.join(dest_dir, f"{base} ({i}){ext}")
        i += 1
    return candidate


def _copy_with_progress(src_file: str, dst_file: str, counters: dict,
                          on_progress, on_speed, should_cancel) -> None:
    """复制单个文件并实时统计进度/速度。

    should_cancel 为可调用对象，返回 True 时中止复制并抛出 Cancelled。
    """
    try:
        size = os.path.getsize(src_file)
    except OSError:
        size = 0
    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
    last_report = time.monotonic()
    last_done = counters["done"]
    with open(src_file, "rb") as fin, open(dst_file, "wb") as fout:
        copied = 0
        while True:
            if should_cancel():
                raise Cancelled()
            chunk = fin.read(CHUNK_SIZE)
            if not chunk:
                break
            fout.write(chunk)
            copied += len(chunk)
            counters["done"] += len(chunk)
            counters["chunk_accum"] += len(chunk)
            now = time.monotonic()
            if now - last_report >= 0.2:
                elapsed_total = now - counters["start"]
                interval = now - last_report
                inst = (counters["done"] - last_done) / interval if interval > 0 else 0
                on_progress(counters["done"], counters["total"])
                on_speed(inst, elapsed_total)
                last_report = now
                last_done = counters["done"]
    # 保持元数据（时间戳等）
    try:
        shutil.copystat(src_file, dst_file)
    except OSError:
        pass
    if size and abs(copied - size) > 0:
        # 复制量异常，记录但不阻塞（已逐字节读取，通常一致）
        pass


def _restore_from_target(target: str, src: str, is_dir: bool) -> None:
    """链接创建失败时，把已复制的目标数据还原回原始位置，保持原路径有效。"""
    try:
        if is_dir:
            shutil.copytree(target, src)
        else:
            shutil.copy2(target, src)
    except OSError:
        pass
    try:
        if is_dir:
            shutil.rmtree(target, ignore_errors=True)
        else:
            os.remove(target)
    except OSError:
        pass


def _move_item(src: str, dest_dir: str, counters: dict,
                on_progress, on_speed, on_item_start, on_log,
                should_cancel) -> bool:
    """迁移单个源项（文件或文件夹）。

    流程：复制（带进度且校验完整性）-> 删除原始源 -> 在原位置建符号链接
    -> 校验链接。若建链接失败，则从目标把数据还原回原位置，保证原路径不失效。
    复制阶段被取消时，清理半拷贝目标并保留原始源不动，返回 False。
    """
    name = os.path.basename(src.rstrip("\\/")) or src
    is_dir = os.path.isdir(src)
    src_size = total_size(src)

    target = _unique_dest(dest_dir, name)
    on_item_start(name)

    # 1) 复制（带进度）
    try:
        if is_dir:
            for rel in _iter_files(src):
                if should_cancel():
                    raise Cancelled()
                s = os.path.join(src, rel)
                d = os.path.join(target, rel)
                _copy_with_progress(s, d, counters, on_progress, on_speed,
                                    should_cancel)
        else:
            _copy_with_progress(src, target, counters, on_progress, on_speed,
                                should_cancel)
    except Cancelled:
        on_log(f"已取消：清理半拷贝目标并保留原始文件 {name}")
        try:
            if is_dir:
                shutil.rmtree(target, ignore_errors=True)
            else:
                os.remove(target)
        except OSError:
            pass
        return False

    # 2) 校验复制完整性（大小一致）
    if total_size(target) != src_size:
        on_log(f"错误：复制到目标后校验不一致：{src} -> {target}")
        try:
            if is_dir:
                shutil.rmtree(target, ignore_errors=True)
            else:
                os.remove(target)
        except OSError:
            pass
        return False

    # 3) 删除原始源（此时原路径已空闲，可安全建立链接）
    try:
        if is_dir:
            shutil.rmtree(src)
        else:
            os.remove(src)
    except OSError as e:
        on_log(f"错误：复制成功但无法删除原始源：{src} ({e})")
        _restore_from_target(target, src, is_dir)
        return False

    # 4) 在原位置建立符号链接 -> 目标
    try:
        symlink_mod.create_symlink(target, src, target_is_directory=is_dir)
    except OSError as e:
        on_log(f"错误：创建符号链接失败，已还原原始文件：{src} -> {target} ({e})")
        _restore_from_target(target, src, is_dir)
        return False

    # 5) 校验链接有效性
    if not symlink_mod.verify_symlink(src, target_is_directory=is_dir):
        on_log(f"错误：符号链接已创建但无法访问，已还原原始文件：{src} -> {target}")
        try:
            if is_dir:
                os.rmdir(src)
            else:
                os.remove(src)
        except OSError:
            pass
        _restore_from_target(target, src, is_dir)
        return False

    on_log(f"完成：{name} -> {target}（原位置已建立符号链接）")
    return True


def migrate(sources: list, dest_dir: str, callbacks: dict) -> dict:
    """执行整体迁移。

    callbacks 可包含：on_progress, on_speed, on_item_start, on_log,
    on_finished, on_error, on_cancelled, on_total, should_cancel
    """
    def cb(name, default=None):
        return callbacks.get(name, lambda *a, **k: None)

    on_progress = cb("on_progress")
    on_speed = cb("on_speed")
    on_item_start = cb("on_item_start")
    on_log = cb("on_log")
    on_finished = cb("on_finished")
    on_error = cb("on_error")
    on_cancelled = cb("on_cancelled")
    on_total = cb("on_total")
    should_cancel = cb("should_cancel", default=lambda: False)

    on_log("正在计算总大小…")
    total = sum(total_size(s) for s in sources)
    on_total(total)
    counters = {
        "done": 0,
        "total": total,
        "start": time.monotonic(),
        "chunk_accum": 0,
    }

    success = 0
    errors = 0
    aborted = False
    for src in sources:
        if should_cancel():
            aborted = True
            break
        if not os.path.exists(src):
            on_log(f"跳过（不存在）：{src}")
            errors += 1
            continue
        try:
            if _move_item(src, dest_dir, counters, on_progress, on_speed,
                          on_item_start, on_log, should_cancel):
                success += 1
            else:
                errors += 1
        except Cancelled:
            aborted = True
            break
        except Exception as e:
            on_error(f"迁移失败：{src} ({e})")
            errors += 1

    # 最终进度
    on_progress(counters["done"], counters["total"])
    elapsed = time.monotonic() - counters["start"]
    overall = counters["done"] / elapsed if elapsed > 0 else 0
    on_speed(overall, elapsed)
    if aborted:
        on_cancelled(success, errors)
    else:
        on_finished(success, errors)
    return {"success": success, "errors": errors, "aborted": aborted,
            "done_bytes": counters["done"], "total_bytes": total}


def _remove_symlink(link: str, is_dir: bool) -> None:
    """仅删除符号链接本身（不触碰目标数据）。"""
    if is_dir:
        os.rmdir(link)
    else:
        os.unlink(link)


def _restore_symlink(link: str, target: str, is_dir: bool) -> None:
    """在 link 处重建指向 target 的符号链接（用于失败回滚）。"""
    try:
        symlink_mod.create_symlink(target, link, target_is_directory=is_dir)
    except OSError:
        pass


def relocate(symlink_path: str, new_dest_dir: str, callbacks: dict) -> dict:
    """修改已迁移项的数据存放位置。

    symlink_path 是当前仍存在的符号链接（原位置），其指向真实数据。
    本函数把真实数据移动到 new_dest_dir（保留名称），再把 symlink_path
    重新指向新的位置，使原路径上的引用继续有效。
    """
    def cb(name, default=None):
        return callbacks.get(name, lambda *a, **k: None)

    on_progress = cb("on_progress")
    on_speed = cb("on_speed")
    on_item_start = cb("on_item_start")
    on_log = cb("on_log")
    on_finished = cb("on_finished")
    on_error = cb("on_error")
    on_cancelled = cb("on_cancelled")
    on_total = cb("on_total")
    should_cancel = cb("should_cancel", default=lambda: False)

    def _fail(msg):
        on_error(msg)
        on_log(msg)
        on_finished(0, 1)
        return {"success": 0, "errors": 1, "done_bytes": 0, "total_bytes": 0}

    if not os.path.islink(symlink_path):
        return _fail(f"所选路径不是符号链接，无法修改其指向：{symlink_path}")
    if not os.path.exists(symlink_path):
        return _fail(f"符号链接路径不存在：{symlink_path}")

    current_target = os.path.realpath(symlink_path)
    if not os.path.exists(current_target):
        return _fail(f"符号链接当前指向的目标已不存在：{current_target}")

    is_dir = os.path.isdir(symlink_path)
    name = os.path.basename(symlink_path.rstrip("\\/")) or symlink_path
    new_target = _unique_dest(new_dest_dir, name)

    on_log("正在计算总大小…")
    total = total_size(current_target)
    on_total(total)
    counters = {
        "done": 0,
        "total": total,
        "start": time.monotonic(),
        "chunk_accum": 0,
    }

    on_item_start(name)

    # 1) 复制真实数据到新位置（带进度）
    try:
        if is_dir:
            for rel in _iter_files(current_target):
                if should_cancel():
                    raise Cancelled()
                s = os.path.join(current_target, rel)
                d = os.path.join(new_target, rel)
                _copy_with_progress(s, d, counters, on_progress, on_speed,
                                    should_cancel)
        else:
            _copy_with_progress(current_target, new_target, counters,
                                on_progress, on_speed, should_cancel)
    except Cancelled:
        on_log("已取消：清理半拷贝目标，原始数据保持不动")
        try:
            if is_dir:
                shutil.rmtree(new_target, ignore_errors=True)
            else:
                os.remove(new_target)
        except OSError:
            pass
        on_cancelled(0, 0)
        return {"success": 0, "errors": 0, "aborted": True,
                "done_bytes": counters["done"], "total_bytes": total}
    except Exception as e:
        on_log(f"复制过程中出错：{e}")
        try:
            if is_dir:
                shutil.rmtree(new_target, ignore_errors=True)
            else:
                os.remove(new_target)
        except OSError:
            pass
        return _fail(f"复制失败：{e}")

    # 2) 校验复制完整性
    if total_size(new_target) != total:
        on_log("复制校验不一致，已回滚")
        try:
            if is_dir:
                shutil.rmtree(new_target, ignore_errors=True)
            else:
                os.remove(new_target)
        except OSError:
            pass
        return _fail("复制校验不一致，未做任何改动")

    # 3) 删除旧符号链接
    try:
        _remove_symlink(symlink_path, is_dir)
    except OSError as e:
        on_log(f"无法删除旧符号链接：{e}")
        try:
            if is_dir:
                shutil.rmtree(new_target, ignore_errors=True)
            else:
                os.remove(new_target)
        except OSError:
            pass
        return _fail(f"删除旧符号链接失败：{e}")

    # 4) 建立指向新位置的符号链接
    try:
        symlink_mod.create_symlink(new_target, symlink_path,
                                   target_is_directory=is_dir)
    except OSError as e:
        on_log(f"创建新符号链接失败，尝试恢复原链接：{e}")
        _restore_symlink(symlink_path, current_target, is_dir)
        try:
            if is_dir:
                shutil.rmtree(new_target, ignore_errors=True)
            else:
                os.remove(new_target)
        except OSError:
            pass
        return _fail(f"创建新符号链接失败：{e}")

    if not symlink_mod.verify_symlink(symlink_path, target_is_directory=is_dir):
        on_log("新符号链接无法访问，恢复原链接")
        try:
            _remove_symlink(symlink_path, is_dir)
        except OSError:
            pass
        _restore_symlink(symlink_path, current_target, is_dir)
        try:
            if is_dir:
                shutil.rmtree(new_target, ignore_errors=True)
            else:
                os.remove(new_target)
        except OSError:
            pass
        return _fail("新符号链接校验失败，已恢复原状")

    # 5) 删除旧的真实数据
    try:
        if is_dir:
            shutil.rmtree(current_target, ignore_errors=True)
        else:
            os.remove(current_target)
    except OSError as e:
        on_log(f"警告：新链接已建立，但删除旧数据失败：{current_target} ({e})")

    on_log(f"完成位置修改：{name} 现在指向 {new_target}")
    on_finished(1, 0)
    return {"success": 1, "errors": 0,
            "done_bytes": counters["done"], "total_bytes": total}

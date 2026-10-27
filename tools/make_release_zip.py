#!/usr/bin/env python3
"""打包发布用 zip：只收录 git 跟踪的文件（含自带 python/ 与 packages/）。

用法：
    python tools/make_release_zip.py            # 输出 dist/Infinite-Canvas-UDG-<版本>-win.zip
    python tools/make_release_zip.py --output D:/xxx.zip

打包内容 = `git ls-files` 列表（工作区当前内容），因此：
- 自动排除 .git/、API/.env（密钥）、assets/（用户素材）、data/canvases 等运行数据、START.exe
- 自动包含 python/ 便携运行时与 packages/ 离线依赖，解压即可双击 start.bat 使用
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import zipfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_version() -> str:
    path = os.path.join(BASE_DIR, "VERSION")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip() or "0.0.0"
    except OSError:
        return "0.0.0"


def tracked_files() -> list[str]:
    """返回 git 跟踪的文件（相对路径，正斜杠）。优先 git，失败时退回目录遍历。"""
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=BASE_DIR,
            capture_output=True,
            check=True,
        ).stdout
        files = [p.decode("utf-8", "replace") for p in out.split(b"\0") if p]
        if files:
            return files
    except (OSError, subprocess.CalledProcessError):
        print("git 不可用，改用目录遍历（可能多收运行数据）", file=sys.stderr)

    skip_dirs = {".git", "__pycache__", ".build_pyi", "dist", "assets", "conversations"}
    skip_top_files = {".env"}
    result: list[str] = []
    for root, dirs, names in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        rel_root = os.path.relpath(root, BASE_DIR).replace("\\", "/")
        for name in names:
            if name in skip_top_files or name.endswith(".pyc"):
                continue
            rel = name if rel_root == "." else f"{rel_root}/{name}"
            result.append(rel)
    return result


def make_zip(output: str) -> tuple[int, int]:
    version = read_version()
    files = tracked_files()
    root = f"Infinite-Canvas-UDG-{version}"
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)

    total_bytes = 0
    missing = 0
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for rel in files:
            src = os.path.join(BASE_DIR, rel.replace("/", os.sep))
            if not os.path.isfile(src):
                missing += 1
                continue
            info = zipfile.ZipInfo.from_file(src, arcname=f"{root}/{rel}")
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(src, "rb") as f:
                data = f.read()
            total_bytes += len(data)
            zf.writestr(info, data)

    if missing:
        print(f"警告：{missing} 个跟踪文件在工作区缺失，已跳过", file=sys.stderr)
    return len(files) - missing, total_bytes


def main() -> int:
    parser = argparse.ArgumentParser(description="打包 Infinite-Canvas-UDG 发布 zip")
    version = read_version()
    parser.add_argument(
        "--output",
        default=os.path.join(BASE_DIR, "dist", f"Infinite-Canvas-UDG-{version}-win.zip"),
        help="输出 zip 路径（默认 dist/Infinite-Canvas-UDG-<版本>-win.zip）",
    )
    args = parser.parse_args()

    count, raw_bytes = make_zip(args.output)
    zip_bytes = os.path.getsize(args.output)
    print(f"已打包 {count} 个文件")
    print(f"原始体积 {raw_bytes / 1024 / 1024:.1f} MB -> zip {zip_bytes / 1024 / 1024:.1f} MB")
    print(f"输出：{args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

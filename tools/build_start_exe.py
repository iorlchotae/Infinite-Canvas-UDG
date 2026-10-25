"""一键打包 START.exe（内嵌图标）。用法：
  python tools/build_start_exe.py [图标ico] [输出exe名]
默认：图标 icons/v2-proposal-b.ico，输出 START.exe 到项目根目录。
依赖 PyInstaller（装在隔离环境 iconbuild 里，不污染项目自带 python）。
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = r"C:/Users/iorlchoate/.workbuddy/binaries/python/envs/iconbuild/Scripts/python.exe"
BUILD = os.path.join(ROOT, ".build_pyi")


def main():
    icon = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "icons", "v2-proposal-b.ico")
    out_name = sys.argv[2] if len(sys.argv) > 2 else "START.exe"
    # PyInstaller 会把自己切到 workpath，相对路径会失效，必须转绝对路径
    icon = os.path.abspath(icon)
    if not os.path.isfile(icon):
        raise SystemExit("图标不存在: %s" % icon)

    if os.path.isdir(BUILD):
        shutil.rmtree(BUILD, ignore_errors=True)

    cmd = [
        PY, "-m", "PyInstaller",
        "--onefile", "--noconsole", "--clean", "--noupx",
        "--name", os.path.splitext(out_name)[0],
        "--icon", icon,
        "--distpath", ROOT,
        "--workpath", BUILD,
        "--specpath", BUILD,
        os.path.join(ROOT, "tools", "start_launcher.py"),
    ]
    print("[build]", " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit("打包失败")
    exe = os.path.join(ROOT, out_name)
    print("[ok]", exe, "%.1f MB" % (os.path.getsize(exe) / 1048576))
    # 清掉中间产物，只留 exe
    shutil.rmtree(BUILD, ignore_errors=True)
    for name in ("start_launcher.spec",):
        p = os.path.join(ROOT, name)
        if os.path.isfile(p):
            os.remove(p)


if __name__ == "__main__":
    main()

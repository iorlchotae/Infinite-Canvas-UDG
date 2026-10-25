"""START.exe 启动器（由 tools/build_start_exe.py 用 PyInstaller 打包，图标内嵌）。
职责单一：找到同目录下的 start.bat 并用 cmd 调起它，依赖自检、端口探测、起服务全部仍由 start.bat 负责。
直接以脚本方式运行也可：python tools/start_launcher.py
"""
import os
import subprocess
import sys


def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    base = app_dir()
    bat = os.path.join(base, "start.bat")
    if not os.path.isfile(bat):
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0,
                "未找到 start.bat，请把 START.exe 与 start.bat 放在同一目录。\n\n路径：%s" % bat,
                "无限画布-联创四院",
                0x10,
            )
        except Exception:
            pass
        return 1
    # 让 start.bat 在自己的控制台窗口里跑（依赖安装、端口探测、启动日志都看得见）
    subprocess.Popen(["cmd.exe", "/c", "start.bat"], cwd=base)
    return 0


if __name__ == "__main__":
    sys.exit(main())

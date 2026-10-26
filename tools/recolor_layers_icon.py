"""终选图标：把 layers.ico 的蓝色强调 (#72B6FF) 重着色为联创红 (#C8102E)。
- 浅灰砖体 (#F4F5F7)、深灰图层 (#54565B)、圆角、抗锯齿边缘全部原样保留
- 按「蓝色覆盖率」线性插值：纯蓝核心 -> 纯红，边缘混合像素按比例偏移，不会出现色边
- 逐尺寸保留原生画作（16/24/32/48/64/128/256），不从 256 缩档
- 手动组装 PNG payload 的 ICO，与源文件格式一致（Windows Vista+ 原生支持）
源文件默认取用户本机 E:\\AI\\设计方案\\C_line_accent\\layers.ico，缺失时回退 icons/ref/layers.png（仅 256 一档）。
输出（icons/）：final-start.ico、final-start.png（256）、final-start-light.png、final-start-dark.png
用法：./python/python.exe tools/recolor_layers_icon.py
"""
import io
import os
import struct
import sys

from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "icons")
SRC = r"E:\AI\设计方案\C_line_accent\layers.ico"
FALLBACK = os.path.join(OUT, "ref", "layers.png")

BLUE = (114, 182, 255)          # 源图强调色（纯平涂）
RED = (200, 16, 46)             # 联创红 #C8102E
DIFF = RED[2] - BLUE[2]         # B 通道差值范围约 [-141, 141]，用 (B-R) 估覆盖率
THRESH = 8                      # (B-R) <= 8 视为非蓝（砖体 3、深灰 7），避免灰被染红


def recolor(img):
    """蓝 -> 红，覆盖率线性插值，alpha 原样保留。"""
    img = img.convert("RGBA")
    r, g, b, a = img.split()
    # 覆盖率: clip((B-R-8)*255/133, 0, 255)
    cov = ImageChops.subtract(b, r)
    cov = cov.point(lambda v: 0 if v <= THRESH else min(255, (v - THRESH) * 255 // (141 - THRESH)))
    # new_c = c + cov*(RED_c-BLUE_c)/255，逐通道整数运算
    def scaled(band, delta):
        return band.point(lambda v: v * abs(delta) // 255)
    out_r = ImageChops.add(r, scaled(cov, RED[0] - BLUE[0])) if RED[0] > BLUE[0] \
        else ImageChops.subtract(r, scaled(cov, BLUE[0] - RED[0]))
    out_g = ImageChops.add(g, scaled(cov, RED[1] - BLUE[1])) if RED[1] > BLUE[1] \
        else ImageChops.subtract(g, scaled(cov, BLUE[1] - RED[1]))
    out_b = ImageChops.add(b, scaled(cov, RED[2] - BLUE[2])) if RED[2] > BLUE[2] \
        else ImageChops.subtract(b, scaled(cov, BLUE[2] - RED[2]))
    return Image.merge("RGBA", (out_r, out_g, out_b, a))


def extract_frames():
    """逐尺寸原生提取（每个 size 重新打开文件，避免 ICO 插件帧缓存问题）。"""
    frames = []
    if os.path.isfile(SRC):
        im = Image.open(SRC)
        sizes = sorted(im.ico.sizes(), key=lambda s: s[0])
        for size in sizes:
            im = Image.open(SRC)
            im.size = size
            im.load()
            frames.append((size[0], im.convert("RGBA")))
        print("[src]", SRC, "->", [s for s, _ in frames])
    else:
        print("[warn] 源 ico 不存在，回退", FALLBACK)
        im = Image.open(FALLBACK).convert("RGBA")
        frames.append((im.width, im))
    return frames


def save_ico(frames, path):
    """手动组装 ICO：PNG payload + 标准 ICONDIR/ICONDIRECTORY，尺寸升序。"""
    entries, payloads = [], []
    offset = 6 + 16 * len(frames)
    for size, img in frames:
        buf = io.BytesIO()
        img.save(buf, "PNG")
        data = buf.getvalue()
        w = 0 if size >= 256 else size
        entries.append(struct.pack("<BBBBHHII", w, w, 0, 0, 1, 32, len(data), offset))
        payloads.append(data)
        offset += len(data)
    with open(path, "wb") as f:
        f.write(struct.pack("<HHH", 0, 1, len(frames)))
        for e in entries:
            f.write(e)
        for p in payloads:
            f.write(p)
    print("[ok]", path, "%.1f KB, %d sizes" % (os.path.getsize(path) / 1024, len(frames)))


def main():
    frames = extract_frames()
    out_frames = [(size, recolor(img)) for size, img in frames]
    save_ico(out_frames, os.path.join(OUT, "final-start.ico"))

    master = dict(out_frames)[max(s for s, _ in out_frames)]
    master.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT, "final-start.png"))
    for bg, tag in (((244, 245, 247, 255), "light"), ((32, 36, 44, 255), "dark")):
        canvas = Image.new("RGBA", (512, 512), bg)
        canvas.alpha_composite(master.resize((512, 512), Image.LANCZOS), (0, 0))
        canvas.convert("RGB").save(os.path.join(OUT, "final-start-%s.png" % tag))

    # QA：输出中不应再有蓝色，红色像素数应等于输入蓝色像素数
    src_blue = out_red = 0
    for size, img in frames:
        for y in range(0, size, 2):
            for x in range(0, size, 2):
                p = img.getpixel((x, y))
                if p[3] > 200 and p[2] > 150 and p[2] - p[0] > 60:
                    src_blue += 1
    for size, img in out_frames:
        for y in range(0, size, 2):
            for x in range(0, size, 2):
                p = img.getpixel((x, y))
                if p[3] > 200 and p[0] > 150 and p[0] - max(p[1], p[2]) > 60:
                    out_red += 1
                assert not (p[3] > 200 and p[2] > 150 and p[2] - p[0] > 60), "残留蓝色!"
    print("[qa] 蓝色样本 %d -> 红色样本 %d %s" % (src_blue, out_red, "OK" if src_blue == out_red else "MISMATCH"))


if __name__ == "__main__":
    main()

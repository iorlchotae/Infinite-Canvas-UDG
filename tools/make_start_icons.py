"""START.BAT 图标方案生成：4 个方向，沿用主程序「黑色圆角画布 + 联创红 #C8102E + UDG」视觉语言。
输出（项目根 icons/ 目录）：
  proposal-{a,b,c,d}.ico   多尺寸图标（16/24/32/48/64/128/256）
  preview-{a,b,c,d}.png    256px 预览
  sheet.png                浅/深底对比总览（含方案名）
用法：./python/python.exe tools/make_start_icons.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")
os.makedirs(OUT, exist_ok=True)

S = 1024                      # 超采样画布
INK = (17, 17, 19, 255)       # 画布黑（比纯黑更耐看）
RED = (200, 16, 46, 255)      # 联创红 #C8102E
WHITE = (255, 255, 255, 255)
RADIUS = 0.225                # 圆角比例，与 static/images/logo.png 的 squircle 一致
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_CN = "C:/Windows/Fonts/msyhbd.ttc"

def squircle(img, color, radius_ratio=RADIUS):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, img.height - 1],
                        radius=int(img.width * radius_ratio), fill=color)
    return img

def play_triangle(d, cx, cy, w, h, color):
    x0, y0 = cx - w / 2, cy - h / 2
    d.polygon([(x0 + w * 0.16, y0), (x0 + w, cy), (x0 + w * 0.16, y0 + h)], fill=color)

def dot(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

# ---------- 方案 A：画布启动键（黑底 + 白点 + 红色播放三角） ----------
def proposal_a():
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    squircle(im, INK)
    d = ImageDraw.Draw(im)
    dot(d, S * 0.44, S * 0.5, S * 0.085, WHITE)              # 像素白点（主程序 LOGO 基因）
    play_triangle(d, S * 0.60, S * 0.5, S * 0.26, S * 0.30, RED)
    return im

# ---------- 方案 B：UDG 品牌徽标（联创红底 + 白字，对应左下角徽标） ----------
def proposal_b():
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    squircle(im, RED)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT_BOLD, int(S * 0.30))
    d.text((S * 0.5, S * 0.5), "UDG", font=f, fill=WHITE, anchor="mm")
    return im

# ---------- 方案 C：像素画布（黑底 + 2x2 像素格，右下格点红） ----------
def proposal_c():
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    squircle(im, INK)
    d = ImageDraw.Draw(im)
    cell, gap = S * 0.20, S * 0.075
    total = cell * 2 + gap
    x0 = (S - total) / 2
    y0 = (S - total) / 2
    for i in range(2):
        for j in range(2):
            x = x0 + i * (cell + gap)
            y = y0 + j * (cell + gap)
            color = RED if (i == 1 and j == 1) else WHITE   # 右下角点亮
            d.rounded_rectangle([x, y, x + cell, y + cell],
                                radius=int(cell * 0.24), fill=color)
    return im

# ---------- 方案 D：画框启动（黑底 + 白色画框 + 红色播放三角） ----------
def proposal_d():
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    squircle(im, INK)
    d = ImageDraw.Draw(im)
    m = S * 0.22
    d.rounded_rectangle([m, m, S - m, S - m],
                        radius=int(S * 0.07), outline=WHITE, width=int(S * 0.042))
    play_triangle(d, S * 0.5, S * 0.5, S * 0.27, S * 0.31, RED)
    return im

PROPOSALS = [
    ("a", "A 画布启动键", proposal_a),
    ("b", "B UDG徽标", proposal_b),
    ("c", "C 像素画布", proposal_c),
    ("d", "D 画框启动", proposal_d),
]

SIZES = [16, 24, 32, 48, 64, 128, 256]
BG_LIGHT = (245, 246, 248, 255)
BG_DARK = (32, 36, 44, 255)

for key, _name, fn in PROPOSALS:
    master = fn()
    master.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT, f"preview-{key}.png"))
    master.resize((256, 256), Image.LANCZOS).save(
        os.path.join(OUT, f"proposal-{key}.ico"), sizes=[(s, s) for s in SIZES])
    print(f"[ok] proposal-{key}.ico / preview-{key}.png")

# ---------- 对比总览：浅色/深色底 + 方案名 ----------
ICON_PX, CELL, PAD, GAP = 128, 150, 20, 24
rows = []
for bg in (BG_LIGHT, BG_DARK):
    cells = []
    for key, name, fn in PROPOSALS:
        box = Image.new("RGBA", (CELL, CELL + 34), bg)
        box.alpha_composite(fn().resize((ICON_PX, ICON_PX), Image.LANCZOS),
                            ((CELL - ICON_PX) // 2, 0))
        label = ImageDraw.Draw(box)
        try:
            f = ImageFont.truetype(FONT_CN, 20)
        except Exception:
            f = ImageFont.load_default()
        label.text((CELL / 2, CELL + 17), name, font=f, fill=(30, 34, 40, 255), anchor="mm")
        cells.append(box)
    width = PAD * 2 + len(cells) * CELL + (len(cells) - 1) * GAP
    row = Image.new("RGBA", (width, CELL + 34 + PAD * 2), (0, 0, 0, 0))
    x = PAD
    for c in cells:
        row.alpha_composite(c, (x, PAD))
        x += CELL + GAP
    rows.append(row)

sheet = Image.new("RGBA", (rows[0].width, rows[0].height * 2 + 24), (0, 0, 0, 0))
for i, r in enumerate(rows):
    sheet.alpha_composite(r, (0, i * (r.height + 24)))
sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.LANCZOS)
sheet.save(os.path.join(OUT, "sheet.png"))
print("[ok] sheet.png", sheet.size)

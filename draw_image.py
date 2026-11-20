#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

One image summing up Friday 20 November 2026, drawn with Pillow from the
verified stories in research.md. Run: python3 draw_image.py
Writes entry.png next to this file (deterministic bytes).
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (250, 246, 236)
INK = (18, 18, 20)
NAVY = (16, 38, 76)
RED = (178, 34, 34)
TEAL = (0, 110, 110)
GOLD = (176, 132, 30)
GREY = (90, 90, 92)
RULE = (150, 146, 136)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def panel(draw, x, y, w, h, fill=(255, 255, 255)):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=fill, outline=RULE, width=2)


def kicker(draw, x, y, text, color=RED):
    f = font(BOLD, 17)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + 24


def headline(draw, x, y, text, size, max_w, fill=INK):
    f = font(BOLD, size)
    return text_block(draw, x, y, text, f, max_w, fill=fill,
                      leading=int(size * 1.15))


def subhead(draw, x, y, text, size, max_w):
    f = font(REG, size)
    return text_block(draw, x, y, text, f, max_w, fill=(48, 48, 52),
                      leading=int(size * 1.25))


# ---- small drawn illustrations (simple vector shapes) ----

def draw_globe_clock(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 80, 140),
              outline=NAVY, width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=(255, 255, 255), width=2)
    d.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14],
              outline=GOLD, width=4)
    d.line([cx, cy, cx + int(r * 0.55), cy - int(r * 0.6)], fill=GOLD, width=5)
    d.line([cx, cy, cx - int(r * 0.4), cy + int(r * 0.3)], fill=GOLD, width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD)


def draw_document_seal(d, x, y, s):
    d.rounded_rectangle([x, y, x + s, y + int(s * 1.25)], radius=6,
                        fill=(255, 255, 255), outline=NAVY, width=3)
    for i in range(3):
        d.line([x + 12, y + 18 + i * 16, x + s - 12, y + 18 + i * 16],
               fill=GREY, width=3)
    d.ellipse([x + s - 34, y + int(s * 1.25) - 34, x + s - 6, y + int(s * 1.25) - 6],
              fill=RED)


def draw_tower_burst(d, x, y, w, h):
    d.rectangle([x + w * 0.15, y + h * 0.35, x + w * 0.4, y + h], fill=NAVY)
    d.rectangle([x + w * 0.5, y + h * 0.1, x + w * 0.75, y + h], fill=(40, 70, 120))
    d.rectangle([x + w * 0.8, y + h * 0.5, x + w * 0.95, y + h], fill=NAVY)
    for i in range(5):
        yy = y + h * 0.2 + i * h * 0.14
        d.line([x + w * 0.55, yy, x + w * 0.7, yy], fill=(255, 220, 100), width=3)
    cx, cy = x + w * 0.72, y + 4
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([cx, cy, cx + int(16 * math.cos(a)), cy + int(16 * math.sin(a))],
               fill=RED, width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)


def draw_cyclone(d, cx, cy, r):
    import math
    for k in range(3):
        pts = []
        for t in range(0, 540, 6):
            a = math.radians(t)
            rr = r * (1 - t / 720.0)
            pts.append((cx + rr * math.cos(a + k * 2.1),
                        cy + rr * math.sin(a + k * 2.1)))
        d.line(pts, fill=TEAL if k % 2 == 0 else NAVY, width=5)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED)


def draw_probe(d, x, y, w, h):
    for i in range(14):
        d.ellipse([x + i * 4, y + h - 6 - i * 2, x + i * 4 + 3, y + h - 3 - i * 2],
                  fill=GOLD)
    d.polygon([(x + w * 0.55, y + h * 0.15), (x + w * 0.95, y + h * 0.45),
               (x + w * 0.55, y + h * 0.75)], fill=(200, 200, 210),
              outline=NAVY)
    d.line([x + w * 0.55, y + h * 0.45, x + w * 0.15, y + h * 0.45],
           fill=NAVY, width=4)
    d.ellipse([x + w * 0.05, y + h * 0.35, x + w * 0.25, y + h * 0.55],
              outline=NAVY, width=3)
    for sx, sy in [(x + 8, y + 8), (x + w - 14, y + 14), (x + w * 0.3, y + 6)]:
        d.ellipse([sx, sy, sx + 5, sy + 5], fill=NAVY)


def draw_game(d, x, y, w, h):
    d.ellipse([x, y, x + w, y + h], fill=(232, 120, 40))
    d.ellipse([x + 8, y + 8, x + w - 8, y + h - 8], outline=(255, 255, 255), width=3)
    f = font(BOLD, int(h * 0.55))
    d.text((x + w * 0.5, y + h * 0.42), "VI", font=f, fill=(255, 255, 255),
           anchor="mm")


def draw_talks(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w * 0.55, y + h * 0.5], radius=10,
                        fill=(255, 255, 255), outline=NAVY, width=3)
    d.rounded_rectangle([x + w * 0.35, y + h * 0.45, x + w, y + h * 0.95],
                        radius=10, fill=(230, 238, 250), outline=NAVY, width=3)
    for i, yy in enumerate([y + 14, y + 30]):
        d.line([x + 12, yy, x + w * 0.55 - 14, yy], fill=GREY, width=3)
    for i, yy in enumerate([y + h * 0.45 + 14, y + h * 0.45 + 30]):
        d.line([x + w * 0.35 + 12, yy, x + w - 14, yy], fill=GREY, width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    f_title = font(BOLD, 62)
    d.text((512, 52), "THE WORLD TODAY", font=f_title, fill=(255, 255, 255),
           anchor="mm")
    f_date = font(BOLD, 24)
    d.text((512, 100), "FRIDAY  20  NOVEMBER  2026", font=f_date,
           fill=(255, 210, 90), anchor="mm")
    d.line([24, 130, W - 24, 130], fill=INK, width=3)

    # ---- lead story: Trump defers Iran decision ----
    panel(d, 24, 144, 976, 252)
    d.rectangle([24, 144, 24 + 976, 144 + 6], fill=RED)
    y = kicker(d, 44, 162, "Lead — Washington")
    y = headline(d, 44, y, "Trump puts Iran decision off to 2027",
                 40, 600)
    y = subhead(d, 44, y + 6,
                "“No rush,” the president says — he will “see what "
                "happens” after 1 January, as the world waits on war or "
                "a deal.", 19, 600)
    draw_globe_clock(d, 880, 272, 78)

    # ---- row 1: three panels ----
    y0, ph = 412, 226
    pw, gap = 312, 20
    # peace declaration
    x = 24
    panel(d, x, y0, pw, ph)
    yy = kicker(d, x + 16, y0 + 14, "Shenzhen")
    yy = headline(d, x + 16, yy, "Trump, Putin & Xi issue joint peace declaration",
                  23, pw - 32)
    subhead(d, x + 16, yy + 4,
            "A day after their historic three-way summit, the leaders "
            "publish a shared statement.", 15, pw - 32)
    draw_document_seal(d, x + pw - 66, y0 + ph - 66, 44)
    # Riyadh strike
    x = 24 + pw + gap
    panel(d, x, y0, pw, ph)
    yy = kicker(d, x + 16, y0 + 14, "Riyadh")
    yy = headline(d, x + 16, yy, "Houthis strike Riyadh; wealth-fund tower hit",
                  23, pw - 32)
    subhead(d, x + 16, yy + 4,
            "Saudi capital attacked; the wealth fund's tower is hit.",
            15, pw - 32)
    draw_tower_burst(d, x + pw - 100, y0 + ph - 64, 84, 48)
    # Cyclone Akvan
    x = 24 + 2 * (pw + gap)
    panel(d, x, y0, pw, ph)
    yy = kicker(d, x + 16, y0 + 14, "India — Cyclone Akvan")
    yy = headline(d, x + 16, yy, "300,000 evacuated as cyclone nears Odisha",
                  23, pw - 32)
    subhead(d, x + 16, yy + 4,
            "Rescue teams deployed; landfall expected today on the "
            "eastern coast.", 15, pw - 32)
    draw_cyclone(d, x + pw - 46, y0 + ph - 40, 28)

    # ---- row 2: three panels ----
    y0 = 654
    x = 24
    panel(d, x, y0, pw, ph)
    yy = kicker(d, x + 16, y0 + 14, "Space")
    yy = headline(d, x + 16, yy, "Voyager 1 passes one light-day from Earth",
                  23, pw - 32)
    subhead(d, x + 16, yy + 4,
            "NASA confirms the farthest human-made object reaches the "
            "milestone, 48 years on.", 15, pw - 32)
    draw_probe(d, x + pw - 104, y0 + ph - 76, 88, 60)
    x = 24 + pw + gap
    panel(d, x, y0, pw, ph)
    yy = kicker(d, x + 16, y0 + 14, "Culture — Games")
    yy = headline(d, x + 16, yy, "GTA 6 sales pass $1.8bn, beating The Odyssey",
                  23, pw - 32)
    subhead(d, x + 16, yy + 4,
            "Rockstar's blockbuster overtakes the biggest film opening "
            "in history.", 15, pw - 32)
    draw_game(d, x + pw - 76, y0 + ph - 72, 60, 60)
    x = 24 + 2 * (pw + gap)
    panel(d, x, y0, pw, ph)
    yy = kicker(d, x + 16, y0 + 14, "Europe")
    yy = headline(d, x + 16, yy, "Europe ready for Ukraine peace talks with Russia",
                  23, pw - 32)
    subhead(d, x + 16, yy + 4,
            "Leaders signal they are open to negotiations to end the "
            "war.", 15, pw - 32)
    draw_talks(d, x + pw - 104, y0 + ph - 72, 88, 56)

    # ---- ticker ----
    d.rectangle([0, 896, W, H], fill=NAVY)
    f_tick = font(BOLD, 19)
    d.text((24, 916), "ALSO TODAY", font=f_tick, fill=(255, 210, 90))
    ticker = ("Hayabusa2 engine trouble ends asteroid landing plan  •  "
              "US & Venezuela restore military cooperation  •  "
              "Migrant boat sinks off Senegal, dozens missing  •  "
              "Van Gogh sells for a record $190.4m  •  "
              "Modi meets the Prince & Princess of Wales  •  "
              "Nicholls 113* as NZ host India in Wellington")
    y = 948
    y = text_block(d, 24, y, ticker, font(REG, 17), W - 48,
                   fill=(235, 235, 235), leading=24)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    data = open(out, "rb").read()
    print("wrote", out, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest()[:16])
    print("size", img.size)


if __name__ == "__main__":
    build()

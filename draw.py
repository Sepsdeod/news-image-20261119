#!/usr/bin/env python3
"""Draw the front page for Thursday 19 November 2026.

Original artwork, drawn from scratch with Pillow: a newspaper-style
poster summarising the day's world news. No photographs, no copied art.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (22, 22, 26)
NAVY = (18, 32, 64)
RED = (178, 34, 34)
GREY = (90, 86, 78)
LINE = (200, 192, 175)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading=None):
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x, y, w, color=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=color, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((512, 26), "THE WORLD IN ONE DAY", font=font(SERIF, 58),
       fill=(250, 246, 236), anchor="ma")
d.text((512, 96), "THURSDAY  19  NOVEMBER  2026", font=font(SANS, 30),
       fill=(232, 196, 106), anchor="ma")
rule(d, 24, 148, W - 48, color=RED, width=6)

# ------------------------------------------------------- lead: GTA VI panel
LX, LY, LW, LH = 24, 168, 976, 330
# Sunset sky over Vice City: gradient bands
sky = [(255, 122, 69), (255, 94, 110), (196, 58, 140), (94, 48, 130),
       (38, 32, 96)]
band_h = 150 // len(sky)
for i, c in enumerate(sky):
    d.rectangle([LX, LY + i * band_h, LX + LW, LY + (i + 1) * band_h],
                fill=c)
# sun
d.ellipse([LX + 700, LY + 18, LX + 820, LY + 138], fill=(255, 214, 120))
d.ellipse([LX + 712, LY + 30, LX + 808, LY + 126], fill=(255, 236, 170))
# skyline silhouettes
import random
random.seed(19)
base = LY + 150
for x in range(LX, LX + LW, 46):
    bh = random.randint(38, 118)
    d.rectangle([x, base - bh, x + 40, base], fill=(30, 18, 64))
    for wy in range(base - bh + 8, base - 6, 16):
        for wx in range(x + 6, x + 34, 12):
            if random.random() < 0.45:
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 214, 120))
# palm trees
def palm(px, py, s, col=(16, 40, 28)):
    d.line([(px, py), (px + 6 * s, py - 46 * s)], fill=col, width=max(3, 4 * s))
    for ang in (-70, -35, 0, 35, 70):
        a = math.radians(ang - 90)
        ex = px + 6 * s + math.cos(a) * 34 * s
        ey = py - 46 * s + math.sin(a) * 16 * s
        d.line([(px + 6 * s, py - 46 * s), (ex, ey)], fill=col, width=max(2, 3 * s))
palm(LX + 40, base, 1)
palm(LX + 120, base, 1)
palm(LX + 900, base, 1)
# sea strip
d.rectangle([LX, base, LX + LW, LY + 168], fill=(24, 90, 110))
d.rectangle([LX, base, LX + LW, LY + 172], fill=(255, 214, 120))
# neon sign
d.text((LX + 488, LY + 178), "VICE CITY", font=font(SANS, 46),
       fill=(255, 240, 120), anchor="ma",
       stroke_width=2, stroke_fill=(255, 120, 180))
# lead text block below the picture
TY = LY + 224
d.text((LX, TY), "GRAND THEFT AUTO VI IS HERE",
       font=font(SERIF, 44), fill=INK)
para(d, LX, TY + 56,
     "After 13 years, Rockstar's sequel unlocks at midnight around the "
     "world — about 17 million copies already sold for $1.65 billion, "
     "and critics score it 99 out of 100.",
     font(SANS_R, 24), INK, LW, leading=31)
rule(d, 24, 512, W - 48, color=LINE, width=2)

# ------------------------------------------------------------- story grid
GX, GY = 24, 530
CW, CH, GAP = 480, 186, 16

stories = [
    ("UNITED STATES", (178, 34, 34),
     "JEFFRIES SET TO MAKE HISTORY",
     "Democrats nominate Hakeem Jeffries for Speaker — "
     "he would be the first Black Speaker of the US House.",
     "capitol"),
    ("THE HAGUE", (18, 32, 64),
     "WORLD COURT RULES TODAY",
     "The ICJ delivers its judgment in The Gambia v. Myanmar — "
     "whether Myanmar committed genocide against the Rohingya.",
     "scales"),
    ("INDIA", (24, 90, 110),
     "CYCLONE AKVAN BEARS DOWN",
     "The storm is set to cross India's east coast between "
     "Machilipatnam and Puri; railways and ports on alert.",
     "cyclone"),
    ("EUROPE", (120, 90, 20),
     "EU PLANS €45BN UKRAINE LOAN",
     "Brussels proposes a loan to cover Kyiv's budget gap, "
     "to be repaid once Russia pays reparations.",
     "stars"),
]


def icon_capitol(d, x, y, s, col):
    d.ellipse([x + 18 * s, y, x + 62 * s, y + 22 * s], fill=col)
    d.rectangle([x + 14 * s, y + 20 * s, x + 66 * s, y + 26 * s], fill=col)
    for i in range(5):
        cx = x + (16 + i * 13) * s
        d.rectangle([cx, y + 26 * s, cx + 6 * s, y + 52 * s], fill=col)
    d.rectangle([x + 8 * s, y + 52 * s, x + 72 * s, y + 58 * s], fill=col)
    d.rectangle([x + 4 * s, y + 58 * s, x + 76 * s, y + 64 * s], fill=col)


def icon_scales(d, x, y, s, col):
    d.line([(x + 40 * s, y + 4 * s), (x + 40 * s, y + 62 * s)],
           fill=col, width=4)
    d.line([(x + 8 * s, y + 12 * s), (x + 72 * s, y + 12 * s)],
           fill=col, width=4)
    for cx in (16, 64):
        d.line([(x + cx * s, y + 12 * s), (x + cx * s, y + 30 * s)],
               fill=col, width=3)
        d.arc([x + (cx - 14) * s, y + 24 * s, x + (cx + 14) * s, y + 52 * s],
              0, 180, fill=col, width=3)
    d.rectangle([x + 26 * s, y + 62 * s, x + 54 * s, y + 68 * s], fill=col)


def icon_cyclone(d, x, y, s, col):
    for r in range(6, 34, 6):
        d.arc([x + 40 * s - r * s, y + 32 * s - r * s,
               x + 40 * s + r * s, y + 32 * s + r * s],
              200, 200 + 300, fill=col, width=3)
    for i in range(3):
        d.line([(x + (10 + i * 22) * s, y + 66 * s),
                (x + (6 + i * 22) * s, y + 76 * s)], fill=col, width=3)


def icon_stars(d, x, y, s, col):
    for k in range(12):
        a = math.radians(k * 30 - 90)
        cx = x + 40 * s + math.cos(a) * 26 * s
        cy = y + 34 * s + math.sin(a) * 26 * s
        d.ellipse([cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s], fill=col)
    d.text((x + 40 * s, y + 22 * s), "€", font=font(SANS, int(26 * s)),
           fill=col, anchor="mm")


ICONS = {"capitol": icon_capitol, "scales": icon_scales,
         "cyclone": icon_cyclone, "stars": icon_stars}

for i, (kicker, kc, head, body, icon) in enumerate(stories):
    cx = GX + (i % 2) * (CW + GAP)
    cy = GY + (i // 2) * (CH + GAP)
    d.rectangle([cx, cy, cx + CW, cy + CH], outline=LINE, width=2)
    d.text((cx + 14, cy + 12), kicker, font=font(SANS, 19), fill=kc)
    ICONS[icon](d, cx + CW - 108, cy + 14, 1, kc)
    head_lines = wrap(d, head, font(SERIF, 27), CW - 128)
    hy = cy + 40
    for line in head_lines:
        d.text((cx + 14, hy), line, font=font(SERIF, 27), fill=INK)
        hy += 32
    para(d, cx + 14, hy + 8, body, font(SANS_R, 19), (52, 50, 46),
         CW - 28, leading=23)

# ------------------------------------------------------------ bottom strip
BY = GY + 2 * CH + GAP + 8
d.rectangle([24, BY, 500, BY + 62], fill=NAVY)
d.text((40, BY + 8), "SPACE", font=font(SANS, 18), fill=(232, 196, 106))
d.text((40, BY + 30), "Voyager 1 reaches one light-day from Earth",
       font=font(SANS_R, 19), fill=(250, 246, 236))
d.rectangle([524, BY, 1000, BY + 62], fill=NAVY)
d.text((540, BY + 8), "SUMMIT", font=font(SANS, 18), fill=(232, 196, 106))
d.text((540, BY + 30), "Trump, Xi and Putin meet in Shenzhen",
       font=font(SANS_R, 19), fill=(250, 246, 236))

# ------------------------------------------------------------------ footer
FY = BY + 62 + 14
d.text((512, FY), "All six stories reported on Thursday 19 November 2026.",
       font=font(SANS_R, 18), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png")

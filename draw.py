#!/usr/bin/env python3
"""Draw the 19 November 2026 front page: one original 1024x1024 poster.

Layout: navy masthead with THE WORLD + the date, a lead panel on the GTA VI
launch (drawn Vice City sunset skyline), then a 2x3 grid of story cards with
simple drawn icons, short headlines and one-line subs, and a footer strip.
Everything is drawn with Pillow primitives; no photos, no copied artwork.
Deterministic: no randomness, no timestamps baked into the image.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
INK = (24, 24, 24)
RULE = (180, 170, 150)


def font(name, size):
    for path in (
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf",
        f"/usr/share/fonts/{name}.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fb(size):
    return font("DejaVuSans-Bold", size)


def fr(size):
    return font("DejaVuSans", size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, kind, ix, iy, accent):
    d.rectangle([ix, iy, ix + 34, iy + 34], outline=accent, width=3)
    if kind == "capitol":
        d.pieslice([ix + 7, iy + 4, ix + 27, iy + 20], 180, 360, fill=accent)
        d.rectangle([ix + 6, iy + 20, ix + 28, iy + 30], fill=accent)
    elif kind == "scales":
        d.line([(ix + 17, iy + 4), (ix + 17, iy + 30)], fill=accent, width=3)
        d.line([(ix + 5, iy + 8), (ix + 29, iy + 8)], fill=accent, width=3)
        d.polygon([(ix + 5, iy + 8), (ix + 11, iy + 20), (ix + 1, iy + 20)],
                  outline=accent)
        d.polygon([(ix + 29, iy + 8), (ix + 33, iy + 20), (ix + 23, iy + 20)],
                  outline=accent)
    elif kind == "storm":
        for r in (4, 9, 14):
            d.arc([ix + 17 - r, iy + 17 - r, ix + 17 + r, iy + 17 + r],
                  20, 300, fill=accent, width=3)
    elif kind == "stars":
        for k in range(8):
            a = math.radians(k * 45)
            sx = ix + 17 + int(11 * math.cos(a))
            sy = iy + 17 + int(11 * math.sin(a))
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=accent)
    elif kind == "probe":
        d.polygon([(ix + 8, iy + 26), (ix + 17, iy + 6), (ix + 26, iy + 26)],
                  outline=accent)
        d.line([(ix + 17, iy + 6), (ix + 26, iy + 2)], fill=accent, width=2)
        d.ellipse([ix + 25, iy + 1, ix + 29, iy + 5], fill=accent)
    else:  # summit skyline
        d.rectangle([ix + 4, iy + 16, ix + 12, iy + 30], fill=accent)
        d.rectangle([ix + 13, iy + 10, ix + 21, iy + 30], fill=accent)
        d.rectangle([ix + 22, iy + 18, ix + 30, iy + 30], fill=accent)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 124], fill=GOLD)
    d.text((W // 2, 52), "THE WORLD", font=fb(84), fill=(255, 255, 255),
           anchor="mm")
    d.text((W // 2, 100), "THURSDAY 19 NOVEMBER 2026",
           font=fb(30), fill=GOLD, anchor="mm")

    # --- lead panel: Vice City sunset ---
    x0, y0, x1, y1 = 28, 142, 996, 470
    for i in range(y1 - y0):
        t = i / (y1 - y0)
        d.line([(x0, y0 + i), (x1, y0 + i)],
               fill=(int(255 - 60 * t), int(120 + 60 * t), int(90 + 110 * t)))
    d.ellipse([452, 168, 572, 288], fill=(255, 214, 90))
    for bx, bw, bh in [(40, 90, 120), (150, 70, 170), (240, 110, 100),
                       (370, 80, 190), (470, 100, 130), (590, 70, 160),
                       (680, 120, 110), (820, 90, 180), (920, 60, 130)]:
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(40, 20, 60))
        for wy in range(y1 - bh + 12, y1 - 8, 18):
            for wx in range(x0 + bx + 10, x0 + bx + bw - 8, 20):
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 214, 90))
    for px in (120, 880):
        d.line([(px, y1), (px, y1 - 70)], fill=(30, 60, 30), width=6)
        for ang in range(-70, 71, 35):
            ex = px + int(48 * math.sin(math.radians(ang)))
            ey = y1 - 70 - int(28 * abs(math.cos(math.radians(ang))))
            d.line([(px, y1 - 70), (ex, ey)], fill=(30, 90, 40), width=5)
    d.rectangle([x0, y1 - 92, x1, y1], fill=NAVY)
    d.text((x0 + 20, y1 - 78), "VICE CITY OPENS ITS DOORS",
           font=fb(40), fill=(255, 255, 255))
    d.text((x0 + 20, y1 - 34),
           "Grand Theft Auto VI launches worldwide after a 13-year wait",
           font=fr(24), fill=(220, 220, 220))

    # --- story grid 2 x 3 ---
    stories = [
        ((20, 33, 61), "JEFFRIES SET TO MAKE HISTORY",
         "Democrat nominated as first Black Speaker of the US House", "capitol"),
        ((120, 40, 40), "WORLD COURT RULES TODAY",
         "ICJ judgment in the Rohingya genocide case v. Myanmar", "scales"),
        ((20, 90, 120), "CYCLONE AKVAN NEARS INDIA",
         "Storm to cross India's east coast near Puri", "storm"),
        ((30, 60, 140), "EU PROPOSES \u20ac45BN UKRAINE LOAN",
         "Brussels seeks funds to cover Kyiv's 2027 budget gap", "stars"),
        ((60, 40, 90), "VOYAGER 1, ONE LIGHT-DAY OUT",
         "NASA probe reaches a record distance from Earth", "probe"),
        ((140, 60, 20), "TRUMP, XI AND PUTIN MEET",
         "Trilateral talks in Shenzhen on the APEC sidelines", "summit"),
    ]
    cw, ch, gx, gy = 308, 148, 28, 490
    for i, (accent, head, sub, icon) in enumerate(stories):
        cx = gx + (i % 3) * (cw + 16)
        cy = gy + (i // 3) * (ch + 14)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10,
                            fill=(255, 255, 255), outline=RULE, width=2)
        d.rectangle([cx, cy, cx + cw, cy + 8], fill=accent)
        tx, ty = cx + 16, cy + 20
        draw_icon(d, icon, tx, ty, accent)
        hy = ty + 2
        for ln in wrap(d, head, fb(21), cw - 66)[:2]:
            d.text((tx + 46, hy), ln, font=fb(21), fill=INK)
            hy += 24
        sy = ty + 78
        for ln in wrap(d, sub, fr(17), cw - 32)[:2]:
            d.text((tx, sy), ln, font=fr(17), fill=(70, 70, 70))
            sy += 21

    # --- footer ---
    d.rectangle([0, 968, W, H], fill=NAVY)
    d.text((W // 2, 996), "THE DAY IN ONE IMAGE  \u00b7  19 NOVEMBER 2026",
           font=fb(22), fill=(255, 255, 255), anchor="mm")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", os.path.getsize("entry.png"), "bytes")


if __name__ == "__main__":
    main()

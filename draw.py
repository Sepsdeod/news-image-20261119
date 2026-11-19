#!/usr/bin/env python3
"""Draw the 19 November 2026 front page, v2: one original 1024x1024 poster.

v2 vs v1 (submitted 01a1f15c, commit a91fc457):
- 9 stories instead of 6, in a 3x3 grid, covering the fuller day:
  added Crimea Bridge third strike, Gulf escalation (Iran vs US bases),
  Bangladesh lockdown violence, UK 1,000-drone pledge for Ukraine.
- ICJ card now reports the delivered verdict (killings, sexual violence,
  genocidal intent "a reasonable inference") instead of "rules today".
- Jeffries card now carries the 251-11 vote; Akvan card carries the
  evacuations; Shenzhen card notes the first-ever trilateral; lead panel
  notes the midnight New Zealand launch and the 99/100 critics' score.
- Dropped Voyager 1: its one-light-day crossing happened on 18 Nov, not
  19 Nov, so it does not belong on a 19 November poster.
- Everything drawn with Pillow primitives; no photos, no copied artwork.
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
    elif kind == "bridge":
        d.arc([ix + 3, iy + 10, ix + 31, iy + 30], 180, 360, fill=accent,
              width=3)
        d.line([(ix + 3, iy + 22), (ix + 31, iy + 22)], fill=accent, width=3)
        d.line([(ix + 9, iy + 22), (ix + 9, iy + 12)], fill=accent, width=2)
        d.line([(ix + 25, iy + 22), (ix + 25, iy + 12)], fill=accent, width=2)
        d.line([(ix + 17, iy + 22), (ix + 17, iy + 8)], fill=accent, width=2)
    elif kind == "missile":
        d.line([(ix + 8, iy + 28), (ix + 26, iy + 8)], fill=accent, width=4)
        d.polygon([(ix + 26, iy + 8), (ix + 30, iy + 4), (ix + 31, iy + 12)],
                  fill=accent)
        d.line([(ix + 8, iy + 28), (ix + 4, iy + 32)], fill=accent, width=3)
        d.line([(ix + 12, iy + 26), (ix + 6, iy + 30)], fill=accent, width=2)
    elif kind == "flame":
        d.polygon([(ix + 17, iy + 3), (ix + 26, iy + 16), (ix + 22, iy + 24),
                   (ix + 27, iy + 30), (ix + 17, iy + 31), (ix + 7, iy + 30),
                   (ix + 12, iy + 24), (ix + 8, iy + 16)], fill=accent)
    elif kind == "drone":
        for cx, cy in ((ix + 7, iy + 7), (ix + 27, iy + 7),
                       (ix + 7, iy + 27), (ix + 27, iy + 27)):
            d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=accent,
                      width=2)
        d.rectangle([ix + 12, iy + 12, ix + 22, iy + 22], fill=accent)
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
    # critics' score badge
    d.rounded_rectangle([x1 - 218, y0 + 14, x1 - 14, y0 + 52], radius=18,
                        fill=GOLD)
    d.text((x1 - 116, y0 + 33), "CRITICS: 99/100", font=fb(20),
           fill=NAVY, anchor="mm")
    d.rectangle([x0, y1 - 92, x1, y1], fill=NAVY)
    d.text((x0 + 20, y1 - 78), "VICE CITY OPENS ITS DOORS",
           font=fb(40), fill=(255, 255, 255))
    d.text((x0 + 20, y1 - 34),
           "GTA VI goes live — first in New Zealand at midnight",
           font=fr(24), fill=(220, 220, 220))

    # --- story grid 3 x 3 ---
    stories = [
        ((120, 40, 40), "ICJ RULES ON ROHINGYA GENOCIDE",
         "Mass killings and sexual violence found; genocidal intent inferred",
         "scales"),
        ((140, 60, 20), "THREE NUCLEAR POWERS, ONE TABLE",
         "Trump, Xi and Putin hold first-ever trilateral in Shenzhen",
         "summit"),
        ((20, 33, 61), "CRIMEA BRIDGE HIT AGAIN",
         "Third strike in a week halts traffic hours before Shenzhen summit",
         "bridge"),
        ((120, 40, 40), "WAR SPREADS ACROSS THE GULF",
         "Iran hits US bases in Kuwait and Bahrain after US strike on Qeshm",
         "missile"),
        ((20, 33, 61), "JEFFRIES NOMINATED 251-11",
         "Democrats' pick for first Black Speaker; floor vote in January",
         "capitol"),
        ((140, 60, 20), "BANGLADESH IN FLAMES",
         "Yunus home torched as lockdown sparks clashes in 28 districts",
         "flame"),
        ((20, 90, 120), "CYCLONE AKVAN BEARS DOWN",
         "50,000+ evacuated as storm nears India's east coast",
         "storm"),
        ((30, 60, 140), "EU OFFERS \u20ac45BN TO KYIV",
         "Loan covers two-thirds of Ukraine's 2027 budget gap",
         "stars"),
        ((60, 40, 90), "UK SENDS 1,000 DRONES TO KYIV",
         "\u00a3260m package unveiled in Berlin; drones fly 1,000km+",
         "drone"),
    ]
    cw, ch, gx, gy = 308, 138, 28, 490
    for i, (accent, head, sub, icon) in enumerate(stories):
        cx = gx + (i % 3) * (cw + 16)
        cy = gy + (i // 3) * (ch + 12)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10,
                            fill=(255, 255, 255), outline=RULE, width=2)
        d.rectangle([cx, cy, cx + cw, cy + 8], fill=accent)
        tx, ty = cx + 16, cy + 18
        draw_icon(d, icon, tx, ty, accent)
        hy = ty + 2
        for ln in wrap(d, head, fb(20), cw - 62)[:2]:
            d.text((tx + 44, hy), ln, font=fb(20), fill=INK)
            hy += 23
        sy = ty + 74
        for ln in wrap(d, sub, fr(16), cw - 32)[:2]:
            d.text((tx, sy), ln, font=fr(16), fill=(70, 70, 70))
            sy += 20

    # --- footer ---
    d.rectangle([0, 968, W, H], fill=NAVY)
    d.text((W // 2, 996),
           "THE DAY IN ONE IMAGE  \u00b7  LATE EDITION  \u00b7  19 NOVEMBER 2026",
           font=fb(22), fill=(255, 255, 255), anchor="mm")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", os.path.getsize("entry.png"), "bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Draw the 19 November 2026 front page, v2 (coordinator rebuild).

One original 1024x1024 poster: "THE WORLD — Thursday 19 November 2026".
Nine stories in a 3x3 grid under a Vice City sunset lead panel.

News verified in-session against live reporting (19 Nov 2026):
- GTA VI launch day; critics 99/100 (Metacritic 99 / OpenCritic 98).
- ICJ delivers its Rohingya judgment: thousands killed, widespread sexual
  violence (Reuters, live from The Hague, 19 Nov).
- First-ever Trump-Xi-Putin trilateral in Shenzhen.
- Crimea Bridge hit for a third time in a week; traffic suspended (Reuters).
- Iran strikes US bases in Kuwait (Ali Al Salem) and Bahrain after the US
  hit Qeshm Island (Reuters).
- Jeffries nominated for Speaker 251-11; floor vote 3 January.
- Bangladesh: Yunus ancestral home torched, 4 killed, clashes in 28
  districts (Reuters).
- Cyclone Akvan: 50,000+ evacuated off India's east coast.
- EU offers EUR 45bn to Kyiv; UK pledges 1,000+ long-range drones
  (GOV.UK, GBP 260m package, Berlin).
Everything is drawn with Pillow primitives; no photos, no copied artwork.
Deterministic: no randomness, no timestamps baked into the image.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
INK = (24, 24, 24)
GREY = (70, 70, 70)
RULE = (180, 170, 150)
WHITE = (255, 255, 255)

# (accent, headline, deck, icon)
STORIES = [
    ((120, 40, 40), "ICJ RULES ON ROHINGYA GENOCIDE",
     "Court finds thousands killed, widespread sexual violence", "scales"),
    ((140, 60, 20), "THREE NUCLEAR POWERS, ONE TABLE",
     "Trump, Xi and Putin hold first-ever trilateral in Shenzhen", "summit"),
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
     "Yunus home torched, 4 killed; clashes in 28 districts",
     "flame"),
    ((20, 90, 120), "CYCLONE AKVAN BEARS DOWN",
     "50,000+ evacuated as storm nears India's east coast", "storm"),
    ((30, 60, 140), "EU OFFERS \u20ac45BN TO KYIV",
     "Loan covers two-thirds of Ukraine's 2027 budget gap", "stars"),
    ((60, 40, 90), "UK SENDS 1,000 DRONES TO KYIV",
     "\u00a3260m package unveiled in Berlin; drones fly 1,000km+", "drone"),
]


def load_font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for folder in ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts"):
        path = os.path.join(folder, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fit_lines(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    out, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def icon(draw, kind, x, y, color):
    """Small 34x34 line icon inside a square frame."""
    draw.rectangle([x, y, x + 34, y + 34], outline=color, width=3)
    if kind == "capitol":
        draw.pieslice([x + 7, y + 4, x + 27, y + 20], 180, 360, fill=color)
        draw.rectangle([x + 6, y + 20, x + 28, y + 30], fill=color)
    elif kind == "scales":
        draw.line([(x + 17, y + 4), (x + 17, y + 30)], fill=color, width=3)
        draw.line([(x + 5, y + 8), (x + 29, y + 8)], fill=color, width=3)
        draw.polygon([(x + 5, y + 8), (x + 11, y + 20), (x + 1, y + 20)],
                     outline=color)
        draw.polygon([(x + 29, y + 8), (x + 33, y + 20), (x + 23, y + 20)],
                     outline=color)
    elif kind == "storm":
        for r in (4, 9, 14):
            draw.arc([x + 17 - r, y + 17 - r, x + 17 + r, y + 17 + r],
                     20, 300, fill=color, width=3)
    elif kind == "stars":
        for k in range(8):
            ang = math.radians(k * 45)
            sx = x + 17 + int(11 * math.cos(ang))
            sy = y + 17 + int(11 * math.sin(ang))
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=color)
    elif kind == "bridge":
        draw.arc([x + 3, y + 10, x + 31, y + 30], 180, 360, fill=color,
                 width=3)
        draw.line([(x + 3, y + 22), (x + 31, y + 22)], fill=color, width=3)
        for vx in (9, 17, 25):
            draw.line([(x + vx, y + 22), (x + vx, y + 12)], fill=color,
                      width=2)
    elif kind == "missile":
        draw.line([(x + 8, y + 28), (x + 26, y + 8)], fill=color, width=4)
        draw.polygon([(x + 26, y + 8), (x + 30, y + 4), (x + 31, y + 12)],
                     fill=color)
        draw.line([(x + 8, y + 28), (x + 4, y + 32)], fill=color, width=3)
    elif kind == "flame":
        draw.polygon([(x + 17, y + 3), (x + 26, y + 16), (x + 22, y + 24),
                      (x + 27, y + 30), (x + 17, y + 31), (x + 7, y + 30),
                      (x + 12, y + 24), (x + 8, y + 16)], fill=color)
    elif kind == "drone":
        for cx, cy in ((x + 7, y + 7), (x + 27, y + 7),
                       (x + 7, y + 27), (x + 27, y + 27)):
            draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=color,
                         width=2)
        draw.rectangle([x + 12, y + 12, x + 22, y + 22], fill=color)
    else:  # summit skyline
        draw.rectangle([x + 4, y + 16, x + 12, y + 30], fill=color)
        draw.rectangle([x + 13, y + 10, x + 21, y + 30], fill=color)
        draw.rectangle([x + 22, y + 18, x + 30, y + 30], fill=color)


def sunset_panel(draw):
    """Lead panel: Vice City sunset over a skyline, with headline band."""
    x0, y0, x1, y1 = 28, 142, 996, 470
    span = y1 - y0
    for i in range(span):
        t = i / span
        draw.line([(x0, y0 + i), (x1, y0 + i)],
                  fill=(int(255 - 60 * t), int(120 + 60 * t),
                        int(90 + 110 * t)))
    draw.ellipse([452, 168, 572, 288], fill=(255, 214, 90))
    skyline = [(40, 90, 120), (150, 70, 170), (240, 110, 100),
               (370, 80, 190), (470, 100, 130), (590, 70, 160),
               (680, 120, 110), (820, 90, 180), (920, 60, 130)]
    for bx, bw, bh in skyline:
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(40, 20, 60))
        for wy in range(y1 - bh + 12, y1 - 8, 18):
            for wx in range(x0 + bx + 10, x0 + bx + bw - 8, 20):
                draw.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 214, 90))
    for px in (120, 880):
        draw.line([(px, y1), (px, y1 - 70)], fill=(30, 60, 30), width=6)
        for ang in range(-70, 71, 35):
            ex = px + int(48 * math.sin(math.radians(ang)))
            ey = y1 - 70 - int(28 * abs(math.cos(math.radians(ang))))
            draw.line([(px, y1 - 70), (ex, ey)], fill=(30, 90, 40), width=5)
    draw.rounded_rectangle([x1 - 218, y0 + 14, x1 - 14, y0 + 52], radius=18,
                           fill=GOLD)
    draw.text((x1 - 116, y0 + 33), "CRITICS: 99/100",
              font=load_font(True, 20), fill=NAVY, anchor="mm")
    draw.rectangle([x0, y1 - 92, x1, y1], fill=NAVY)
    draw.text((x0 + 20, y1 - 78), "VICE CITY OPENS ITS DOORS",
              font=load_font(True, 40), fill=WHITE)
    draw.text((x0 + 20, y1 - 34),
              "GTA VI goes live \u2014 first in New Zealand at midnight",
              font=load_font(False, 24), fill=(220, 220, 220))


def story_card(draw, accent, head, deck, kind, cx, cy, cw, ch):
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10,
                           fill=WHITE, outline=RULE, width=2)
    draw.rectangle([cx, cy, cx + cw, cy + 8], fill=accent)
    tx, ty = cx + 16, cy + 18
    icon(draw, kind, tx, ty, accent)
    hy = ty + 2
    for line in fit_lines(draw, head, load_font(True, 20), cw - 62)[:2]:
        draw.text((tx + 44, hy), line, font=load_font(True, 20), fill=INK)
        hy += 23
    sy = ty + 74
    for line in fit_lines(draw, deck, load_font(False, 16), cw - 32)[:2]:
        draw.text((tx, sy), line, font=load_font(False, 16), fill=GREY)
        sy += 20


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead.
    d.rectangle([0, 0, SIZE, 118], fill=NAVY)
    d.rectangle([0, 118, SIZE, 124], fill=GOLD)
    d.text((SIZE // 2, 52), "THE WORLD", font=load_font(True, 84),
           fill=WHITE, anchor="mm")
    d.text((SIZE // 2, 100), "THURSDAY 19 NOVEMBER 2026",
           font=load_font(True, 30), fill=GOLD, anchor="mm")
    sunset_panel(d)
    # 3x3 story grid.
    cw, ch, gx, gy = 308, 138, 28, 490
    for i, (accent, head, deck, kind) in enumerate(STORIES):
        cx = gx + (i % 3) * (cw + 16)
        cy = gy + (i // 3) * (ch + 12)
        story_card(d, accent, head, deck, kind, cx, cy, cw, ch)
    # Footer.
    d.rectangle([0, 968, SIZE, SIZE], fill=NAVY)
    d.text((SIZE // 2, 996),
           "THE DAY IN ONE IMAGE  \u00b7  LATE EDITION  \u00b7  19 NOVEMBER 2026",
           font=load_font(True, 22), fill=WHITE, anchor="mm")
    img.save("entry.png", optimize=True)
    print("wrote entry.png", os.path.getsize("entry.png"), "bytes")


if __name__ == "__main__":
    build()

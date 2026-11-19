#!/usr/bin/env python3
"""Draw the 19 November 2026 full-day front page, v3 (coordinator rebuild).

One original 1024x1024 poster: "THE WORLD - Thursday 19 November 2026".
Lead: GTA VI launch day. Below it, 35 stories in a 5x7 grid grouped by
region - 36 stories total across 7 regions plus global - each with a short
headline and a one-line deck, colour-coded by region.

Every story was verified in-session against live reporting dated
19 November 2026 (Reuters, AP, BBC, GOV.UK, Politico, Sotheby's/Artnet,
Pew, Save the Children, IAEA, and same-day news digests):
- Kept from v2 (verified): ICJ Rohingya verdict delivered; first-ever
  Trump-Xi-Putin trilateral in Shenzhen; third Crimea Bridge strike;
  Gulf escalation (Iran hits US bases in Kuwait and Bahrain after the US
  strike on Qeshm); Jeffries nominated Speaker 251-11; Bangladesh
  (Yunus home torched, 4 killed, clashes in 28 districts); Cyclone
  Akvan (50,000+ evacuated off India's east coast); EU EUR 45bn loan
  to Kyiv; UK 1,000 long-range drones for Kyiv (GBP 260m, Berlin).
- New for v3: GTA VI launch (critics 99/100) as lead; Van Gogh sells
  for $190.4m, an artist record (Sotheby's New York, reported 19 Nov);
  US-Venezuela military pact signed in Caracas (Hegseth, ties cut in
  2005 restored); Pennsylvania measles passes 1,500 cases; Bay Area
  storm floods San Francisco; isolated Awa group makes rare contact
  in Brazil's Amazon; Panama arrests a second suspect over the attack
  on journalist Rolando Rodriguez's home; Ukraine hits two Russian
  oil refineries (about half of Russia's refining output hit); UK-EU
  summit to mend post-Brexit ties; European Commission hit by a
  cyberattack using the ARTEX AI tool (Politico, 19 Nov); Israel
  crosses the Gaza ceasefire line (Yellow Line); Houthi rocket debris
  damages the Saudi PIF tower in Riyadh; IEA calls the Hormuz crisis
  the greatest threat to energy security; tanker struck in the Strait
  of Hormuz (UKMTO, crew safe); Ethiopia and Eritrea mass troops,
  artillery near disputed Badme; Uganda landslide survivors seek
  justice at the UN; South Korea's top court orders a retrial for
  ex-PM Han Duck-soo (15-year martial-law sentence overturned);
  Russian Tu-95 bombers land in Vietnam after flights near Taiwan
  and Japan; Japan's PM Takaichi cut a lonely figure at APEC;
  North Korea expands uranium enrichment (IAEA); Indonesia passes an
  asset-forfeiture bill; US-Philippines $2bn+ loan package pursued;
  Fiji declares a disaster over El Nino drought; Cyclone Xavier
  nears the Cook Islands (winds near 100 knots); COP31 ministers
  race for a deal in Antalya; 589m children lived in conflict zones
  in 2025 (Save the Children); Pew projects Islam passes Christianity
  as the world's largest faith by 2035.
Everything is drawn with Pillow primitives; no photos, no copied artwork.
Deterministic: no randomness, no timestamps baked into the image.
"""
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

# Region colours.
REGIONS = {
    "N. AMERICA": (20, 33, 61),
    "LATIN AM.": (30, 120, 80),
    "EUROPE": (30, 60, 140),
    "MID. EAST": (140, 60, 20),
    "AFRICA": (160, 110, 20),
    "ASIA": (120, 40, 40),
    "PACIFIC": (20, 90, 120),
    "GLOBAL": (90, 60, 120),
}

# (region, headline, deck)
STORIES = [
    ("N. AMERICA", "JEFFRIES NOMINATED 251-11",
     "Democrats' pick for first Black Speaker"),
    ("N. AMERICA", "VAN GOGH SELLS FOR $190.4M",
     "Blossoming Chestnut Trees sets artist record"),
    ("N. AMERICA", "US, VENEZUELA SIGN MILITARY PACT",
     "Hegseth in Caracas restores ties cut in 2005"),
    ("N. AMERICA", "MEASLES PASSES 1,500 IN PENNSYLVANIA",
     "Outbreak grows; US loses elimination status"),
    ("N. AMERICA", "BAY AREA STORM FLOODS SAN FRANCISCO",
     "Record rain disrupts roads and transit"),
    ("LATIN AM.", "ISOLATED AWA GROUP MAKES CONTACT",
     "Rare encounter in Brazil's Amazon"),
    ("LATIN AM.", "PANAMA ARRESTS SECOND SUSPECT",
     "Attack on journalist Rodriguez's home"),
    ("EUROPE", "EU OFFERS \u20ac45BN TO KYIV",
     "Loan covers two-thirds of Ukraine's 2027 gap"),
    ("EUROPE", "UK SENDS 1,000 DRONES TO KYIV",
     "\u00a3260m Berlin package; drones fly 1,000km+"),
    ("EUROPE", "CRIMEA BRIDGE HIT AGAIN",
     "Third strike in a week halts traffic"),
    ("EUROPE", "UKRAINE HITS TWO RUSSIAN REFINERIES",
     "About half of Russia's refining output hit"),
    ("EUROPE", "UK AND EU SUMMIT TO PATCH TIES",
     "Leaders meet to mend post-Brexit relations"),
    ("EUROPE", "EU COMMISSION HIT BY CYBERATTACK",
     "AI tool ARTEX used; staff data may be exposed"),
    ("MID. EAST", "WAR SPREADS ACROSS THE GULF",
     "Iran hits US bases in Kuwait and Bahrain"),
    ("MID. EAST", "ISRAEL CROSSES GAZA CEASEFIRE LINE",
     "Troops enter Hamas-held central Gaza"),
    ("MID. EAST", "HOUTHI ROCKET DEBRIS HITS RIYADH",
     "Saudi PIF tower damaged; coalition hits Yemen"),
    ("MID. EAST", "IEA: HORMUZ 'GREATEST THREAT'",
     "Energy watchdog warns global supply at risk"),
    ("MID. EAST", "TANKER STRUCK IN STRAIT OF HORMUZ",
     "Engine-room hit near Khasab; crew safe"),
    ("AFRICA", "ETHIOPIA, ERITREA MASS TROOPS",
     "Artillery near disputed Badme raises war fears"),
    ("AFRICA", "UGANDA LANDSLIDE SURVIVORS AT UN",
     "Families seek justice after deadly slide"),
    ("ASIA", "ICJ RULES ON ROHINGYA GENOCIDE",
     "Thousands killed, widespread sexual violence"),
    ("ASIA", "THREE NUCLEAR POWERS, ONE TABLE",
     "First-ever Trump-Xi-Putin talks in Shenzhen"),
    ("ASIA", "BANGLADESH IN FLAMES",
     "Yunus home torched, 4 killed; clashes in 28 districts"),
    ("ASIA", "CYCLONE AKVAN BEARS DOWN",
     "50,000+ evacuated off India's east coast"),
    ("ASIA", "SOUTH KOREA ORDERS HAN RETRIAL",
     "Top court overturns ex-PM's 15-year sentence"),
    ("ASIA", "RUSSIAN BOMBERS LAND IN VIETNAM",
     "Tu-95s arrive after flights near Taiwan, Japan"),
    ("ASIA", "JAPAN'S PM CUT LONELY FIGURE",
     "Takaichi isolated at APEC in Shenzhen"),
    ("ASIA", "NORTH KOREA EXPANDS ENRICHMENT",
     "IAEA warns of growing uranium programme"),
    ("ASIA", "INDONESIA PASSES SEIZURE BILL",
     "Asset forfeiture without a conviction"),
    ("ASIA", "US-PHILIPPINES $2BN LOAN PACKAGE",
     "White House pursues financing for alliance"),
    ("PACIFIC", "FIJI DECLARES DISASTER OVER DROUGHT",
     "El Nino water crisis triggers emergency"),
    ("PACIFIC", "CYCLONE XAVIER NEARS COOK ISLANDS",
     "Winds near 100 knots at the storm's centre"),
    ("GLOBAL", "COP31 MINISTERS RACE FOR A DEAL",
     "Antalya talks stall as ministers meet"),
    ("GLOBAL", "589M CHILDREN LIVED IN CONFLICT",
     "Save the Children: nearly 1 in 4 children in war zones"),
    ("GLOBAL", "ISLAM TO PASS CHRISTIANITY BY 2035",
     "Pew: Muslims to become world's largest faith"),
]


def load_font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for folder in ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts"):
        path = os.path.join(folder, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fit_lines(draw, text, font, width, max_lines):
    """Greedy word wrap, capped at max_lines; warns (and truncates) on overflow."""
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
    if len(out) > max_lines:
        print(f"OVERFLOW ({max_lines} lines max): {text!r} -> {out}")
        out = out[:max_lines]
    return out


def lead_strip(draw):
    """Slim sunset lead strip: GTA VI launch."""
    x0, y0, x1, y1 = 24, 106, 1000, 190
    span = y1 - y0
    for i in range(span):
        t = i / span
        draw.line([(x0, y0 + i), (x1, y0 + i)],
                  fill=(int(255 - 135 * t), int(110 - 60 * t),
                        int(80 + 60 * t)))
    draw.ellipse([880, 112, 936, 168], fill=(255, 214, 90))
    draw.rounded_rectangle([x1 - 190, y0 + 8, x1 - 10, y0 + 34], radius=13,
                           fill=GOLD)
    draw.text((x1 - 100, y0 + 21), "CRITICS: 99/100",
              font=load_font(True, 15), fill=NAVY, anchor="mm")
    draw.text((x0 + 16, y0 + 26), "VICE CITY OPENS ITS DOORS",
              font=load_font(True, 30), fill=WHITE)
    draw.text((x0 + 16, y0 + 62),
              "GTA VI goes live - first in New Zealand at midnight",
              font=load_font(False, 17), fill=WHITE)


def story_card(draw, region, head, deck, cx, cy, cw, ch):
    color = REGIONS[region]
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=8,
                           fill=WHITE, outline=RULE, width=1)
    draw.rectangle([cx + 8, cy, cx + cw - 8, cy + 4], fill=color)
    tx = cx + 10
    draw.text((tx, cy + 9), region, font=load_font(True, 9), fill=color)
    head_lines = fit_lines(draw, head, load_font(True, 15), cw - 20, 3)
    hy = cy + 23
    for line in head_lines:
        draw.text((tx, hy), line, font=load_font(True, 15), fill=INK)
        hy += 17
    max_deck = 2 if len(head_lines) > 1 else 3
    deck_lines = fit_lines(draw, deck, load_font(False, 11), cw - 20,
                           max_deck)
    dy = hy + 2
    for line in deck_lines:
        draw.text((tx, dy), line, font=load_font(False, 11), fill=GREY)
        dy += 13


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead.
    d.rectangle([0, 0, SIZE, 84], fill=NAVY)
    d.rectangle([0, 84, SIZE, 88], fill=GOLD)
    d.text((24, 44), "THE WORLD", font=load_font(True, 56), fill=WHITE,
           anchor="lm")
    d.text((1000, 30), "36 STORIES  \u00b7  7 REGIONS",
           font=load_font(True, 20), fill=GOLD, anchor="rm")
    d.text((1000, 58), "FULL-DAY EDITION",
           font=load_font(True, 20), fill=WHITE, anchor="rm")
    # Region legend strip.
    lx, ly = 24, 93
    d.text((lx, ly), "THURSDAY 19 NOVEMBER 2026",
           font=load_font(True, 13), fill=NAVY)
    rx = 1024 - 24
    for name in reversed(list(REGIONS)):
        label = name.replace("N. AMERICA", "N AMERICA").replace(
            "LATIN AM.", "LATIN AM").replace("MID. EAST", "MID EAST")
        w = d.textlength(label, font=load_font(True, 10))
        rx -= int(w) + 4
        d.rectangle([rx - 12, ly + 1, rx - 2, ly + 11],
                    fill=REGIONS[name])
        d.text((rx, ly), label, font=load_font(True, 10), fill=GREY)
        rx -= 16
    lead_strip(d)
    # 5x7 story grid.
    cw, ch, gx, gy = 187, 104, 24, 198
    for i, (region, head, deck) in enumerate(STORIES):
        cx = gx + (i % 5) * (cw + 9)
        cy = gy + (i // 5) * (ch + 8)
        story_card(d, region, head, deck, cx, cy, cw, ch)
    # Footer.
    d.rectangle([0, 976, SIZE, SIZE], fill=NAVY)
    d.text((SIZE // 2, 1000),
           "THE DAY IN ONE IMAGE  \u00b7  36 STORIES  \u00b7  19 NOVEMBER 2026",
           font=load_font(True, 20), fill=WHITE, anchor="mm")
    img.save("entry.png", optimize=True)
    print("wrote entry.png", os.path.getsize("entry.png"), "bytes")
    print("stories:", len(STORIES) + 1, "(lead + grid)")


if __name__ == "__main__":
    build()

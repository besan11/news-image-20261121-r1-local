#!/usr/bin/env python3
"""Render the Saturday 21 November 2026 front page (1024x1024 PNG).

Draws the whole page with PIL from the story data below: masthead, stats
ticker, region chips, three lead stories with big filled art, ten secondary
panels with solid mini-scenes, a numbered world map, two-column briefs, a
DATE CHECK box and a one-day assertion footer. Run: python3 render.py
writes entry.png next to this file. No network, no input files besides the
DejaVu fonts in fonts/.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
CREAM = (247, 241, 222)
PAPER = (250, 246, 232)
INK = (26, 26, 26)
RED = (163, 30, 34)
NAVY = (22, 41, 77)
TEAL = (14, 122, 107)
GREEN = (46, 125, 50)
OCHRE = (178, 106, 0)
GREY = (90, 90, 90)
RULE = (120, 110, 90)

SERIF = os.path.join(HERE, "fonts", "DejaVuSerif.ttf")
SERIF_B = os.path.join(HERE, "fonts", "DejaVuSerif-Bold.ttf")
SANS = os.path.join(HERE, "fonts", "DejaVuSans.ttf")
SANS_B = os.path.join(HERE, "fonts", "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None, max_lines=None):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    lh = leading or int(fnt.size * 1.22)
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def centred(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def rule(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def chip(draw, x, y, label, count, bg, fg=(255, 255, 255)):
    fnt = font(SANS_B, 12)
    text = "%s %d" % (label, count)
    w = draw.textlength(text, font=fnt) + 16
    draw.rounded_rectangle([x, y, x + w, y + 22], radius=3, fill=bg)
    draw.text((x + 8, y + 4), text, font=fnt, fill=fg)
    return x + w + 6


# ---------------------------------------------------------------- stories
# Every figure below was checked against fresh reporting on 21 Nov 2026
# (Reuters, AP, AFP, CNN, FT, ESA, CoinDesk) before drawing. Items that
# happened on Friday night but were first reported on Saturday are worded
# as reported/announced on Saturday; items first reported 19-20 Nov are
# excluded from the page and named in DATE CHECK instead.

TICKER = [
    ("$60,000", "Bitcoin retakes $60,000"),
    ("$1.8bn", "crypto bets liquidated"),
    ("$7.5bn", "Amazon nears Decart deal"),
    ("69%", "dengue cut in Brazil trial"),
    ("$120bn", "COP31 adaptation target"),
    ("400+", "drones fired at Kyiv"),
]

REGIONS = [
    ("EUROPE", 8, TEAL),
    ("THE AMERICAS", 15, RED),
    ("ASIA-PACIFIC", 3, GREEN),
    ("MIDEAST", 7, OCHRE),
    ("WORLD", 7, GREY),
]

LEADS = [
    {
        "kicker": "1 · BAHRAIN · GULF",
        "head": "Iran strikes US bases in Bahrain",
        "body": ("The IRGC says missiles and drones hit US positions at al-Riffa "
                 "and Awali. Bahrain says a civilian plant was hit, a fire broke "
                 "out and no one was hurt."),
        "tag": "AL-RIFFA · AWALI",
    },
    {
        "kicker": "2 · GUASAVE · CARTELS",
        "head": "Mexico seizes \u2018Chapo Isidro\u2019",
        "body": ("FBI Top 10 fugitive Fausto Isidro Meza Flores was seized in "
                 "Guasave. Eleven died as gunmen fought back; he was flown to "
                 "Mexico City."),
        "tag": "CAPTURED",
    },
    {
        "kicker": "3 · KRYVYI RIH · WAR",
        "head": "Missiles kill a boy in Zelensky\u2019s home city",
        "body": ("Two ballistic missiles hit central Kryvyi Rih; a boy of 7 and "
                 "a woman of 20 were killed and 60 wounded. More rockets fell "
                 "as rescuers worked."),
        "tag": "2 KILLED · 60 WOUNDED",
    },
]

PANELS = [
    {
        "kicker": "4 · HORMUZ · SHIPPING",
        "head": "Two tankers hit in the Strait",
        "body": ("Torkel\u2019s stern and Arina\u2019s engine room hit. No casualties."),
        "kind": "tanker",
    },
    {
        "kicker": "5 · MARKETS · CRYPTO",
        "head": "Bitcoin bounces back above $60,000",
        "body": ("Up 9% from a $55,130 low after $1.8bn of bets were wiped out."),
        "kind": "candles",
    },
    {
        "kicker": "6 · MERCURY · SPACE",
        "head": "BepiColombo reaches Mercury",
        "body": ("Two orbiters enter Mercury\u2019s orbit after an eight-year flight."),
        "kind": "mercury",
    },
    {
        "kicker": "7 · ANTALYA · CLIMATE",
        "head": "COP31 runs past its deadline",
        "body": ("No deal by Saturday; the draft drops fossil fuels and $120bn."),
        "kind": "clock",
    },
    {
        "kicker": "8 · TOKYO · MARKETS",
        "head": "Asia follows Wall Street\u2019s rout",
        "body": ("Nikkei and Kospi fell 5% overnight after Friday\u2019s Nasdaq rout."),
        "kind": "downchart",
    },
    {
        "kicker": "9 · WASHINGTON · DIPLOMACY",
        "head": "Zelensky calls Putin \u2018a killer\u2019",
        "body": ("Trump: Putin is a \u2018friend\u2019. Zelensky: \u2018For us, he is a killer.\u2019"),
        "kind": "flags",
    },
    {
        "kicker": "10 · SEATTLE · TECH",
        "head": "Amazon nears $7.5bn Decart deal",
        "body": ("FT: an announcement could come next week; nothing signed yet."),
        "kind": "deal",
    },
    {
        "kicker": "11 · BELO HORIZONTE · HEALTH",
        "head": "Mosquitoes cut dengue by 69%",
        "body": ("Trial of 5,700 children over four years: infections fell 69%."),
        "kind": "mosquito",
    },
    {
        "kicker": "12 · KHARKIV · WAR",
        "head": "Drone wounds 11 in Kharkiv",
        "body": ("Drone hits a five-storey block; 11 wounded, two are children."),
        "kind": "drone",
    },
    {
        "kicker": "13 · WASHINGTON · CYBER",
        "head": "FBI probes breach of crime database",
        "body": ("Suspected NCIC breach; the second FBI system hit in months."),
        "kind": "shield",
    },
]

BRIEFS = [
    (14, "TORKEL \u2014 Crew evacuated after stern hit."),
    (15, "QESHM \u2014 Iran says it downed a US drone."),
    (16, "SITRA \u2014 US interceptor crashed, big fire."),
    (17, "GUASAVE \u2014 Gunmen set 10 roadblocks ablaze."),
    (18, "REWARD \u2014 US offered $5m for Meza Flores."),
    (19, "POLAND \u2014 Kh-101 fell 50 km from border."),
    (20, "WARSAW \u2014 Rutte: NATO defends every inch."),
    (21, "F-16 \u2014 US denies Iran claim a jet was hit."),
    (22, "PANAMA \u2014 Will block a deal without fossil text."),
    (23, "FINANCE \u2014 $300bn a year by 2035 stands."),
    (24, "TOKYO \u2014 Nikkei falls more than 5% overnight."),
    (25, "SEOUL \u2014 Kospi falls more than 5% overnight."),
    (26, "VIX \u2014 Fear gauge closes at 35.89, a 19-month high."),
    (27, "S&P \u2014 Seventh straight daily fall, worst since 2020."),
    (28, "NVIDIA \u2014 $1.4tn of value gone since 8 Nov."),
    (29, "MERCURY \u2014 Insertion burn fired at 18:24 UTC."),
    (30, "ORBITS \u2014 MPO and Mio part on 9\u201310 December."),
    (31, "TRIAL \u2014 Four years, 58 clusters, 5,700 children."),
    (32, "FLORIDA \u2014 Worst dengue outbreak since the 1940s."),
    (33, "NCIC \u2014 FBI learnt of intrusion earlier this week."),
    (34, "TALKS \u2014 Trump: peace \u2018stuck in the mud\u2019."),
    (35, "BERLIN \u2014 Europeans meet in solidarity with Kyiv."),
    (36, "DOHA \u2014 Qatari envoys carried messages to Tehran."),
    (37, "LAUNCHER \u2014 IRGC shows twin-missile launcher."),
    (38, "DECART \u2014 FT: deal may be announced next week."),
    (39, "DECART \u2014 Founded 2023; $300m raised in May."),
    (40, "BITCOIN \u2014 Still 52% below its October peak."),
]

DATE_CHECK = ("DATE CHECK \u2014 First reported 19\u201320 Nov, so NOT on this page: "
              "the Shenzhen summit of Trump, Xi and Putin \u00b7 the ICJ\u2019s Rohingya "
              "genocide ruling \u00b7 Anthropic\u2019s $83 IPO pricing \u00b7 Russia\u2019s "
              "overnight barrage on Kyiv \u00b7 COP31\u2019s scheduled final day (20 Nov) \u00b7 "
              "BepiColombo\u2019s transfer-module separation (3 Sep).")

FOOTER = ("Every story here happened, or was first reported, on Saturday 21 November 2026.  "
          "Sources: Reuters, AP, AFP, CNN, FT, ESA, CoinDesk.  Original drawings.")


# ------------------------------------------------------------------- art
def burst(draw, cx, cy, r1, r2, n, fill):
    """Starburst polygon: alternating outer/inner radius points."""
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def arc_pts(x0, y0, x1, y1, lift, steps=24):
    """Points along a quadratic arc from (x0,y0) to (x1,y1)."""
    mx, my = (x0 + x1) / 2, min(y0, y1) - lift
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
        pts.append((x, y))
    return pts


def lead_art(img, draw, box, idx):
    """Big filled scene that fills the whole lead frame (no empty sky)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if idx == 0:
        # Bahrain night: navy sky, missile arcs, burning horizon, base.
        draw.rectangle(box, fill=NAVY)
        draw.ellipse([x1 - 92, y0 + 6, x1 - 22, y0 + 76], fill=(255, 176, 66))
        draw.ellipse([x1 - 78, y0 + 20, x1 - 36, y0 + 62], fill=(255, 214, 130))
        for k, (sx, lift, ex) in enumerate([(8, 46, 210), (30, 62, 250), (60, 40, 290)]):
            pts = arc_pts(x0 + sx, y1 - 34, x0 + ex, y1 - 44, lift)
            draw.line(pts, fill=(255, 214, 130), width=4)
            draw.ellipse([pts[-1][0] - 5, pts[-1][1] - 5,
                          pts[-1][0] + 5, pts[-1][1] + 5], fill=(255, 120, 40))
        # Sea + burning horizon + base silhouette.
        draw.rectangle([x0, y1 - 34, x1, y1], fill=(18, 90, 110))
        for bx in range(x0 + 8, x1 - 30, 46):
            draw.polygon([(bx, y1 - 34), (bx + 14, y1 - 58),
                          (bx + 28, y1 - 34)], fill=(255, 120, 40))
        draw.rectangle([x0 + 12, y1 - 52, x0 + 62, y1 - 34], fill=(10, 18, 36))
        draw.rectangle([x0 + 70, y1 - 62, x0 + 96, y1 - 34], fill=(10, 18, 36))
        draw.ellipse([x0 + 104, y1 - 70, x0 + 124, y1 - 50], fill=(200, 210, 220))
        draw.rectangle([x0 + 112, y1 - 52, x0 + 116, y1 - 34], fill=(10, 18, 36))
        tag = font(SANS_B, 15)
        draw.text((x0 + 10, y0 + 8), "AL-RIFFA  ·  AWALI", font=tag, fill=(255, 255, 255))
    elif idx == 1:
        # Guasave night raid: dark red-brown sky, helicopter, searchlight,
        # burning roadblocks along the road.
        draw.rectangle(box, fill=(58, 26, 22))
        # Narrow searchlight cone from the helicopter down to the road.
        draw.polygon([(x0 + 132, y0 + 30), (x0 + 96, y1 - 30),
                      (x0 + 168, y1 - 30)], fill=(255, 226, 150))
        # Helicopter silhouette in pale grey, big in the upper half.
        hx, hy = x0 + 150, y0 + 22
        heli = (216, 206, 192)
        draw.line([(hx - 95, hy), (hx + 95, hy)], fill=heli, width=6)
        draw.ellipse([hx - 56, hy + 2, hx + 56, hy + 32], fill=heli)
        draw.polygon([(hx + 50, hy + 6), (hx + 92, hy + 16),
                      (hx + 50, hy + 26)], fill=heli)
        draw.rectangle([hx - 8, hy + 32, hx + 2, hy + 46], fill=heli)
        draw.rectangle([hx - 36, hy + 32, hx - 26, hy + 46], fill=heli)
        # Road + burning barricades.
        draw.rectangle([x0, y1 - 30, x1, y1], fill=(30, 20, 16))
        draw.line([(x0, y1 - 15), (x1, y1 - 15)], fill=(220, 200, 120), width=2)
        for bx in (x0 + 22, x0 + 120, x0 + 230, x0 + 292):
            draw.rectangle([bx, y1 - 46, bx + 26, y1 - 30], fill=(40, 26, 20))
            burst(draw, bx + 13, y1 - 50, 16, 7, 8, (255, 120, 40))
            burst(draw, bx + 13, y1 - 48, 9, 4, 8, (255, 214, 90))
        # Solid red CAPTURED stamp, rotated, bottom right over the road.
        stamp = Image.new("RGBA", (150, 44), (0, 0, 0, 0))
        sd = ImageDraw.Draw(stamp)
        sd.rectangle([2, 2, 147, 41], fill=(163, 30, 34))
        sd.rectangle([2, 2, 147, 41], outline=(255, 255, 255), width=2)
        sd.text((12, 8), "CAPTURED", font=font(SANS_B, 24), fill=(255, 255, 255))
        stamp = stamp.rotate(10, expand=True, resample=Image.BICUBIC)
        img.paste(stamp, (x0 + w - 172, y0 + 62), stamp)
    else:
        # Kryvyi Rih: dark slate, one huge missile streak, broken blocks,
        # red casualty banner across the bottom of the art.
        draw.rectangle(box, fill=(43, 43, 52))
        pts = arc_pts(x0 + 16, y0 + 96, x1 - 30, y0 + 18, -30)
        draw.line(pts, fill=(255, 214, 130), width=5)
        draw.ellipse([pts[-1][0] - 7, pts[-1][1] - 7,
                      pts[-1][0] + 7, pts[-1][1] + 7], fill=(255, 120, 40))
        burst(draw, x1 - 30, y0 + 18, 26, 11, 10, (255, 140, 50))
        burst(draw, x1 - 30, y0 + 18, 14, 6, 10, (255, 220, 120))
        # Broken apartment blocks along the bottom.
        for bx, bh, tilt in [(x0 + 10, 52, 0), (x0 + 78, 66, 0),
                             (x0 + 150, 44, 0), (x0 + 214, 58, 0),
                             (x0 + 272, 48, 0)]:
            draw.rectangle([bx, y1 - 34 - bh, bx + 56, y1 - 30],
                           fill=(16, 16, 22))
            for wy in range(y1 - 34 - bh + 8, y1 - 36, 14):
                for wx in (bx + 8, bx + 26, bx + 42):
                    draw.rectangle([wx, wy, wx + 8, wy + 8],
                                   fill=(255, 176, 66))
        draw.rectangle([x0, y1 - 30, x1, y1], fill=RED)
        centred(draw, (x0 + x1) / 2, y1 - 25, "2 KILLED  ·  60 WOUNDED",
                font(SANS_B, 15), fill=(255, 255, 255))


def panel_art(draw, box, kind):
    """One solid mini-scene per secondary panel (never a thin icon)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx = int((x0 + x1) / 2)
    if kind == "tanker":
        draw.rectangle(box, fill=(18, 90, 110))
        draw.rectangle([x0, y0 + h - 18, x1, y1], fill=(10, 60, 78))
        draw.rectangle([x0 + 22, y0 + 26, x1 - 22, y0 + 44], fill=(16, 16, 22))
        draw.rectangle([x0 + 30, y0 + 12, x0 + 52, y0 + 26], fill=(16, 16, 22))
        burst(draw, x1 - 40, y0 + 22, 14, 6, 8, (255, 120, 40))
        burst(draw, x1 - 40, y0 + 24, 7, 3, 8, (255, 214, 90))
        for wx in range(x0 + 6, x1 - 6, 26):
            draw.arc([wx, y0 + h - 12, wx + 22, y0 + h + 2],
                     180, 360, fill=(255, 255, 255), width=2)
    elif kind == "candles":
        draw.rectangle(box, fill=(16, 84, 48))
        bars = [(56, 22, 1), (74, 16, 0), (92, 24, 1), (110, 14, 0),
                (128, 20, 1), (146, 16, 0)]
        for bx, bh, up in bars:
            col = (120, 220, 140) if up else (255, 90, 80)
            draw.rectangle([x0 + bx, y0 + h - 8 - bh, x0 + bx + 12, y0 + h - 8],
                           fill=col)
            draw.line([(x0 + bx + 6, y0 + h - 14 - bh),
                       (x0 + bx + 6, y0 + h - 2)], fill=col, width=2)
        draw.text((x0 + 8, y0 + 4), "+9%", font=font(SANS_B, 20),
                  fill=(255, 255, 255))
    elif kind == "mercury":
        draw.rectangle(box, fill=(8, 8, 14))
        for sx, sy in [(14, 10), (40, 26), (150, 8), (172, 30), (120, 6)]:
            draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                         fill=(255, 255, 255))
        draw.ellipse([cx - 26, y0 + 6, cx + 26, y0 + 58], fill=(214, 120, 50))
        draw.ellipse([cx - 14, y0 + 14, cx - 4, y0 + 24], fill=(170, 80, 30))
        draw.ellipse([cx + 6, y0 + 32, cx + 16, y0 + 42], fill=(170, 80, 30))
        draw.rectangle([x1 - 46, y0 + 12, x1 - 30, y0 + 18], fill=(220, 220, 230))
        draw.line([(x1 - 38, y0 + 18), (cx + 26, y0 + 30)],
                  fill=(220, 220, 230), width=2)
    elif kind == "clock":
        draw.rectangle(box, fill=(46, 125, 50))
        draw.ellipse([cx - 26, y0 + 4, cx + 26, y0 + 56], fill=(250, 246, 232))
        draw.ellipse([cx - 26, y0 + 4, cx + 26, y0 + 56],
                     outline=(26, 26, 26), width=3)
        draw.line([(cx, y0 + 30), (cx, y0 + 12)], fill=(26, 26, 26), width=3)
        draw.line([(cx, y0 + 30), (cx + 14, y0 + 36)], fill=(26, 26, 26), width=3)
        draw.ellipse([cx - 3, y0 + 27, cx + 3, y0 + 33], fill=RED)
        draw.text((x0 + 6, y0 + 4), "NO", font=font(SANS_B, 16), fill=(255, 255, 255))
        draw.text((x0 + 6, y0 + 22), "DEAL", font=font(SANS_B, 16), fill=(255, 255, 255))
    elif kind == "downchart":
        draw.rectangle(box, fill=(122, 20, 24))
        pts = [(x0 + 8, y0 + 12), (x0 + 50, y0 + 22), (x0 + 90, y0 + 18),
               (x0 + 130, y0 + 34), (x0 + 168, y0 + 48)]
        draw.line(pts, fill=(255, 255, 255), width=4)
        draw.polygon([(x0 + 168, y0 + 48), (x0 + 178, y0 + 40),
                      (x0 + 178, y0 + 52)], fill=(255, 255, 255))
        draw.text((x0 + 8, y0 + 34), "\u22125%", font=font(SANS_B, 20),
                  fill=(255, 255, 255))
    elif kind == "flags":
        # Ukraine flag left, US flag right, split down the middle.
        draw.rectangle([x0, y0, cx, y0 + h // 2], fill=(0, 91, 187))
        draw.rectangle([x0, y0 + h // 2, cx, y1], fill=(255, 213, 0))
        for i in range(7):
            col = RED if i % 2 == 0 else (255, 255, 255)
            draw.rectangle([cx, y0 + i * (h // 7), x1, y0 + (i + 1) * (h // 7)],
                           fill=col)
        draw.rectangle([cx, y0, cx + 52, y0 + h // 2], fill=NAVY)
        for sy in range(y0 + 6, y0 + h // 2 - 4, 9):
            for sx in range(cx + 6, cx + 48, 10):
                draw.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
        draw.text((x0 + 8, y0 + h - 22), "\u201cKILLER\u201d",
                  font=font(SANS_B, 15), fill=(26, 26, 26))
    elif kind == "deal":
        draw.rectangle(box, fill=(232, 120, 20))
        draw.rectangle([x0 + 14, y0 + 30, x0 + 62, y0 + 56], fill=(120, 60, 0))
        draw.rectangle([x0 + 14, y0 + 30, x0 + 62, y0 + 38], fill=(255, 200, 120))
        draw.text((x0 + 70, y0 + 8), "$7.5bn", font=font(SANS_B, 22),
                  fill=(255, 255, 255))
        draw.text((x0 + 70, y0 + 34), "NEARLY", font=font(SANS_B, 13),
                  fill=(255, 255, 255))
    elif kind == "mosquito":
        draw.rectangle(box, fill=(46, 125, 50))
        draw.ellipse([cx - 8, y0 + 18, cx + 8, y0 + 44], fill=(16, 16, 16))
        draw.ellipse([cx - 20, y0 + 8, cx - 2, y0 + 26], fill=(255, 255, 255))
        draw.ellipse([cx + 2, y0 + 8, cx + 20, y0 + 26], fill=(255, 255, 255))
        for lx in (-16, -8, 8, 16):
            draw.line([(cx + lx // 2, y0 + 30), (cx + lx, y0 + 52)],
                      fill=(16, 16, 16), width=2)
    elif kind == "drone":
        draw.rectangle(box, fill=(90, 110, 130))
        draw.rectangle([x0 + 20, y0 + 26, x0 + 84, y0 + 54], fill=(40, 40, 48))
        for wy in range(y0 + 32, y0 + 52, 10):
            for wx in (x0 + 28, x0 + 46, x0 + 64):
                draw.rectangle([wx, wy, wx + 8, wy + 6], fill=(255, 176, 66))
        draw.rectangle([x1 - 58, y0 + 8, x1 - 34, y0 + 16], fill=(16, 16, 16))
        draw.line([(x1 - 66, y0 + 12), (x1 - 26, y0 + 12)], fill=(16, 16, 16),
                  width=3)
        draw.line([(x1 - 46, y0 + 16), (x1 - 46, y0 + 24)], fill=(16, 16, 16),
                  width=3)
        burst(draw, x1 - 30, y0 + 44, 12, 5, 8, (255, 120, 40))
    elif kind == "shield":
        draw.rectangle(box, fill=NAVY)
        draw.polygon([(cx, y0 + 6), (cx + 24, y0 + 14), (cx + 24, y0 + 32),
                      (cx, y0 + 52), (cx - 24, y0 + 32), (cx - 24, y0 + 14)],
                     outline=(255, 255, 255), width=3)
        draw.text((cx - 24, y0 + 20), "NCIC", font=font(SANS_B, 13),
                  fill=(255, 255, 255))
        draw.rectangle([x0 + 8, y0 + 8, x0 + 34, y0 + 22], fill=RED)
        draw.text((x0 + 11, y0 + 9), "2nd", font=font(SANS_B, 11),
                  fill=(255, 255, 255))


# ------------------------------------------------------------------- map
# Simplified continent outlines (equirectangular, lon/lat pairs). Drawn
# from general geography, not traced from any image.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-65, 44), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60),
     (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-40, 76), (-60, 76)],
    [(-80, 9), (-72, 12), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -41), (-70, -54), (-73, -37),
     (-70, -20), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (43, 12),
     (51, 11), (48, 2), (40, -10), (35, -18), (28, -33), (18, -35),
     (12, -18), (9, 4), (-8, 5)],
    [(-10, 36), (-9, 43), (-2, 49), (5, 53), (8, 57), (18, 56), (21, 55),
     (28, 60), (30, 70), (50, 68), (70, 72), (100, 77), (130, 72),
     (160, 70), (178, 66), (162, 60), (140, 40), (127, 35), (120, 30),
     (108, 18), (105, 9), (100, 8), (92, 16), (80, 8), (72, 20), (60, 25),
     (52, 27), (48, 29), (43, 12), (39, 21), (35, 28), (26, 36), (22, 37),
     (12, 44), (3, 43), (-2, 37)],
    [(113, -22), (114, -32), (124, -33), (135, -35), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (136, -12), (132, -11), (126, -14),
     (122, -17), (114, -22)],
    [(95, 5), (98, 8), (100, 6), (97, 2)],          # Sumatra
    [(106, -6), (110, -7), (114, -8), (112, -8)],    # Java
    [(130, -2), (134, -4), (136, -2), (132, 0)],     # New Guinea (west)
    [(139, 36), (141, 38), (140, 42), (142, 44), (144, 43), (141, 39),
     (139, 34)],                                      # Japan (Honshu)
    [(-3, 54), (-5, 50), (1, 51), (1, 53)],          # Britain
]

# (number, lon, lat, dx, dy) — dx/dy nudge the pin label clear of neighbours.
PINS = [
    (1, 50.5, 26.0, 0, 0),
    (2, -108.5, 25.6, 0, 0),
    (3, 33.4, 47.9, 0, 0),
    (4, 56.5, 26.5, 8, 6),
    (5, -74.0, 40.7, 0, 0),
    (6, 8.65, 49.87, 0, -2),
    (7, 30.7, 36.9, 0, 0),
    (8, 139.7, 35.7, 0, 0),
    (9, -77.0, 38.9, -6, 4),
    (10, -122.3, 47.6, 0, 0),
    (11, -43.9, -19.9, 0, 0),
    (12, 36.2, 49.99, 6, -4),
    (13, -77.0, 38.9, 8, -8),
]


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(207, 224, 232))
    lon0, lon1, lat0, lat1 = -180, 180, 78, -58

    def px(lon, lat):
        return (x0 + (lon - lon0) / (lon1 - lon0) * (x1 - x0),
                y0 + (lat0 - lat) / (lat0 - lat1) * (y1 - y0))

    for poly in CONTINENTS:
        draw.polygon([px(lon, lat) for lon, lat in poly],
                     fill=(232, 220, 192), outline=(150, 130, 100))
    num = font(SANS_B, 10)
    for n, lon, lat, dx, dy in PINS:
        cx, cy = px(lon, lat)
        cx, cy = cx + dx, cy + dy
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                     outline=(255, 255, 255), width=1)
        tw = draw.textlength(str(n), font=num)
        draw.text((cx - tw / 2, cy - 7), str(n), font=num,
                  fill=(255, 255, 255))


# ------------------------------------------------------------------ page
def build():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    M = 14                      # outer margin
    X0, X1 = M, W - M
    y = 8

    # Top bar.
    draw.text((X0, y), "THE WORLD IN ONE DAY", font=font(SANS_B, 13), fill=RED)
    right = "SATURDAY\u2019S NEWS  \u00b7  ONE PAGE  \u00b7  40 STORIES"
    rw = draw.textlength(right, font=font(SANS_B, 13))
    draw.text((X1 - rw, y), right, font=font(SANS_B, 13), fill=INK)
    y += 20
    rule(draw, X0, X1, y, fill=INK, width=2)
    y += 6

    # Masthead + sub-dek.
    centred(draw, W / 2, y, "Saturday 21 November 2026",
            font(SERIF_B, 52), fill=INK)
    y += 60
    centred(draw, W / 2, y,
            "Iran hits US bases in Bahrain  \u00b7  Mexico seizes \u2018Chapo Isidro\u2019"
            "  \u00b7  Missiles kill a boy in Zelensky\u2019s home city",
            font(SERIF, 15), fill=RED)
    y += 22
    rule(draw, X0, X1, y, fill=INK, width=2)
    y += 6

    # Stats ticker: six big round numbers only.
    cw = (X1 - X0) / 6
    for i, (num, label) in enumerate(TICKER):
        cx = X0 + cw * i
        if i:
            draw.line([(cx, y + 2), (cx, y + 42)], fill=RULE, width=1)
        centred(draw, cx + cw / 2, y, num, font(SERIF_B, 28), fill=RED)
        para(draw, cx + 8, y + 32, label, font(SANS, 10), cw - 16,
             fill=INK, leading=12, max_lines=1)
    y += 46
    rule(draw, X0, X1, y, fill=INK, width=1)
    y += 6

    # Region strip: coloured chips, counts sum to 40.
    x = X0
    for label, count, bg in REGIONS:
        x = chip(draw, x, y, label, count, bg)
    right = "40 STORIES"
    rw = draw.textlength(right, font=font(SANS_B, 13))
    draw.text((X1 - rw, y + 4), right, font=font(SANS_B, 13), fill=INK)
    y += 26

    # Three leads: big art on top, kicker + headline + body below.
    col_w = int((X1 - X0 - 24) / 3)
    art_h = 110
    for i, lead in enumerate(LEADS):
        lx = int(X0 + i * (col_w + 12))
        lead_art(img, draw, (lx, y, lx + col_w, y + art_h), i)
        ty = y + art_h + 6
        draw.text((lx, ty), lead["kicker"], font=font(SANS_B, 11), fill=RED)
        ty += 15
        ty = para(draw, lx, ty, lead["head"], font(SERIF_B, 21),
                  col_w, fill=INK, leading=22, max_lines=2)
        ty += 2
        para(draw, lx, ty, lead["body"], font(SANS, 12.5), col_w,
             fill=INK, leading=14.5, max_lines=3)
    y += art_h + 6 + 15 + 44 + 2 + 43 + 8

    # Ten secondary panels, two rows of five, each a solid mini-scene.
    pw = int((X1 - X0 - 4 * 10) / 5)
    ph = 124
    for row in range(2):
        for col in range(5):
            p = PANELS[row * 5 + col]
            px0 = int(X0 + col * (pw + 10))
            py0 = y + row * (ph + 6)
            panel_art(draw, (px0, py0, px0 + pw, py0 + 52), p["kind"])
            ty = py0 + 56
            draw.text((px0, ty), p["kicker"], font=font(SANS_B, 9), fill=RED)
            ty += 12
            ty = para(draw, px0, ty, p["head"], font(SERIF_B, 14.5), pw,
                      fill=INK, leading=15.5, max_lines=2)
            para(draw, px0, ty + 1, p["body"], font(SANS, 10.5), pw,
                 fill=INK, leading=11.5, max_lines=2)
    y += 2 * ph + 6 + 6

    # Map + briefs header.
    draw.text((X0, y), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    draw.text((X0 + 296, y), "ALSO ON SATURDAY 21 NOVEMBER \u2014 27 MORE STORIES",
              font=font(SANS_B, 12), fill=RED)
    y += 17
    map_top = y
    map_h = 224
    draw_map(draw, (X0, map_top, X0 + 272, map_top + map_h))
    draw.text((X0, map_top + map_h + 4),
              "Red numbers mark stories 1\u201313. Positions are approximate.",
              font=font(SANS, 10), fill=INK)

    # Briefs: two columns, one dense line each, real detail, no filler.
    bx = X0 + 288
    bw = int((X1 - bx - 12) / 2)
    bf = font(SANS, 11.5)
    rows = (len(BRIEFS) + 1) // 2
    for i, (n, text) in enumerate(BRIEFS):
        col, r = divmod(i, rows)
        xx = bx + col * (bw + 12)
        yy = map_top + r * 16
        draw.text((xx, yy), "%d " % n, font=font(SANS_B, 11.5), fill=RED)
        nw = draw.textlength("%d " % n, font=font(SANS_B, 11.5))
        draw.text((xx + nw, yy), text, font=bf, fill=INK)
    y = map_top + map_h + 20

    # DATE CHECK box.
    rule(draw, X0, X1, y, fill=RED, width=2)
    draw.rectangle([X0, y + 2, X1, y + 40], outline=RED, width=2)
    para(draw, X0 + 8, y + 7, DATE_CHECK, font(SANS, 11.5), X1 - X0 - 16,
         fill=INK, leading=14, max_lines=2)
    y += 44
    rule(draw, X0, X1, y, fill=INK, width=2)
    y += 5
    centred(draw, W / 2, y, FOOTER, font(SANS, 10.5), fill=INK)
    return img


def main():
    img = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

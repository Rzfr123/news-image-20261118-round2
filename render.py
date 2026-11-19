#!/usr/bin/env python3
"""Render the news-image-20261118 round-2 entry: a photo-led newspaper
front page for Wednesday 18 November 2026.

Photojournalism style, after the CNN / Al Jazeera front pages of the day:
white page, black masthead, red kickers, one big lead photograph and four
photo cards, then a three-item briefs strip. All photographs are freely
licensed Wikimedia Commons files committed under assets/ (see README for
attribution); no network is used at render time.

Usage: python3 render.py [output.png]   (default: entry.png next to this file)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width

INK = (17, 17, 17)
PAPER = (255, 255, 255)
RED = (204, 0, 0)
GRAY = (96, 96, 96)
FAINT = (205, 205, 205)
TAG_BG = (17, 17, 17)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)          # noqa: E731
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def cover(im, tw, th, fx=0.5, fy=0.5, box=None):
    """Crop `im` to the target aspect, centred on focus point (fx, fy)
    in relative coordinates, then resize to (tw, th). If `box` is given
    as relative (x0, y0, x1, y1), first cut to that region (used to zoom
    into a distant subject and to crop out a watermark)."""
    if box is not None:
        sw, sh = im.size
        im = im.crop((int(box[0] * sw), int(box[1] * sh),
                      int(box[2] * sw), int(box[3] * sh)))
    sw, sh = im.size
    target = tw / th
    src = sw / sh
    if src > target:  # too wide: cut sides
        nw = int(sh * target)
        x0 = int(min(max(fx * sw - nw / 2, 0), sw - nw))
        box = (x0, 0, x0 + nw, sh)
    else:  # too tall: cut top/bottom
        nh = int(sw / target)
        y0 = int(min(max(fy * sh - nh / 2, 0), sh - nh))
        box = (0, y0, sw, y0 + nh)
    return im.crop(box).resize((tw, th), Image.LANCZOS)


def photo_tag(draw, x, y, label):
    """Small black place tag in the bottom-left corner of a photo."""
    fnt = F_SANS_B(13)
    tw = draw.textlength(label, font=fnt)
    pad, hh = 8, 22
    draw.rectangle([x, y - hh, x + tw + 2 * pad, y], fill=TAG_BG)
    draw.text((x + pad, y - hh + 4), label, font=fnt, fill=PAPER)


def draw_card(draw, img, x, y, w, h, kicker, headline, deck, asset, tag,
              focus, region=None):
    """One 2-column story card: photo left, text right."""
    pw = 200
    pic = cover(Image.open(os.path.join(HERE, "assets", asset)), pw, h,
                *focus, box=region)
    img.paste(pic, (x, y))
    photo_tag(draw, x, y + h, tag)
    tx = x + pw + 12
    tw = w - pw - 12
    cy = y + 2
    draw.text((tx, cy), kicker, font=F_SANS_B(14), fill=RED)
    cy += 20
    for line in wrap(draw, headline, F_SANS_B(22), tw)[:3]:
        draw.text((tx, cy), line, font=F_SANS_B(22), fill=INK)
        cy += 27
    cy += 3
    for line in wrap(draw, deck, F_SANS(15), tw)[:3]:
        draw.text((tx, cy), line, font=F_SANS(15), fill=(51, 51, 51))
        cy += 19


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png")
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead: CNN/Al Jazeera-style top line + big serif date ----
    d.text((MARGIN, 22), "WORLD NEWS", font=F_SANS_B(18), fill=RED)
    right = "WEDNESDAY"
    d.text((W - MARGIN - d.textlength(right, font=F_SANS_B(18)), 22),
           right, font=F_SANS_B(18), fill=GRAY)
    d.text((MARGIN, 46), "18 NOVEMBER 2026", font=F_SERIF_B(64), fill=INK)
    d.text((MARGIN, 122), "The world's news in one image",
           font=F_SERIF(20), fill=GRAY)
    d.rectangle([MARGIN, 150, W - MARGIN, 154], fill=INK)
    d.rectangle([MARGIN, 157, W - MARGIN, 159], fill=RED)

    # ---- Lead story: full-width Shenzhen panorama ----
    # Region crop zooms into the tower cluster and cuts the watermark
    # printed at the panorama's right edge.
    lead = cover(Image.open(os.path.join(HERE, "assets", "shenzhen.jpg")),
                 CW, 244, 0.5, 0.5, box=(0.52, 0.30, 0.88, 0.74))
    img.paste(lead, (MARGIN, 168))
    photo_tag(d, MARGIN, 168 + 244, "SHENZHEN")
    d.text((MARGIN, 424), "SHENZHEN  ·  DIPLOMACY",
           font=F_SANS_B(17), fill=RED)
    d.text((MARGIN, 446), "THREE LEADERS, ONE SUMMIT",
           font=F_SANS_B(40), fill=INK)
    deck = ("Trump lands in China as Xi and Putin meet a day ahead "
            "of the first US\u2013China\u2013Russia three-way talks.")
    cy = 492
    for line in wrap(d, deck, F_SANS(21), CW):
        d.text((MARGIN, cy), line, font=F_SANS(21), fill=(51, 51, 51))
        cy += 27

    d.line([MARGIN, 558, W - MARGIN, 558], fill=FAINT, width=1)

    # ---- Four photo cards, 2 x 2 ----
    cards = [
        ("THE GULF", "IRAN HITS KUWAIT, BAHRAIN",
         "Tehran strikes a US base and Gulf sites after US hits "
         "on Qeshm Island.", "kuwait.jpg", "KUWAIT", (0.5, 0.5),
         (0.26, 0.02, 0.74, 0.64)),
        ("UKRAINE", "KERCH BRIDGE HIT AGAIN",
         "Ukraine strikes the Crimea link; part of the road "
         "span collapses.", "kerch.jpg", "KERCH", (0.40, 0.45), None),
        ("WASHINGTON", "DEMOCRATS TAKE SENATE",
         "Peltola unseats Sullivan in Alaska; Democrats lead "
         "56\u201344.", "capitol.jpg", "WASHINGTON", (0.50, 0.40), None),
        ("GAZA", "TRUCE AT RISK",
         "The Board of Peace warns the Gaza ceasefire is at "
         "risk of collapse.", "gaza.jpg", "GAZA CITY", (0.50, 0.50), None),
    ]
    card_w = (CW - 16) // 2
    card_h = 158
    for i, (kick, head, dk, asset, tag, focus, region) in enumerate(cards):
        cx = MARGIN + (i % 2) * (card_w + 16)
        cy0 = 574 + (i // 2) * (card_h + 14)
        draw_card(d, img, cx, cy0, card_w, card_h, kick, head, dk,
                  asset, tag, focus, region)

    # ---- Briefs strip ----
    d.line([MARGIN, 914, W - MARGIN, 914], fill=INK, width=2)
    briefs = [
        ("EBOLA", "Outbreak in DR Congo passes 11,000 cases."),
        ("ANTHROPIC", "Raises a record $81.3bn in a stock offering."),
        ("MEASLES", "US loses measles-free status after 26 years."),
    ]
    bw = (CW - 2 * 16) // 3
    for i, (kick, txt) in enumerate(briefs):
        bx = MARGIN + i * (bw + 16)
        d.text((bx, 926), kick, font=F_SANS_B(15), fill=RED)
        by = 946
        for line in wrap(d, txt, F_SANS(15), bw):
            d.text((bx, by), line, font=F_SANS(15), fill=(51, 51, 51))
            by += 19

    # ---- Footer: photo credits ----
    d.text((MARGIN, 988),
           "Photos: Wikimedia Commons \u2014 Shenzhen: Sparktour (CC BY-SA 4.0); "
           "Kuwait Towers: Gladiator2030 (CC BY-SA 4.0); Kerch Bridge: Alexxx1979",
           font=F_SANS(11), fill=GRAY)
    d.text((MARGIN, 1001),
           "(CC BY-SA 4.0); US Capitol: Noclip (public domain); Gaza City: "
           "OneArmedMan (public domain).",
           font=F_SANS(11), fill=GRAY)

    img.save(out, "PNG")
    print(f"wrote {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()

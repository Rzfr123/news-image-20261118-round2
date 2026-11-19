#!/usr/bin/env python3
"""Render news-image-20261118 round 2 rev 1: broadsheet flyer with
broadcast accents. One 1024x1024 RGB image summarising the world's news
on Wednesday 18 November 2026. Python + Pillow, DejaVu fonts.
Deterministic: no timestamps, no randomness."""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

W, H = 1024, 1024
OUT = "entry.png"

INK = (16, 16, 18)
PAPER = (250, 248, 243)
RED = (198, 12, 24)
DARK = (12, 18, 34)          # navy nameplate / lower third / ticker
GREY = (90, 88, 84)
RULE = (200, 196, 188)
WHITE = (255, 255, 255)
MUTE = (176, 182, 198)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
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


def fit_cover(path, tw, th, x0_frac=0.5, boost=1.0, zoom=1.0):
    """Focus-point centre crop, then resize to cover tw x th.
    zoom > 1 crops tighter (closer) before resizing."""
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    target = tw / th
    if sw / sh > target:  # too wide: crop width
        cw = int(sh * target / zoom)
        x0 = int((sw - cw) * x0_frac)
        box = (x0, 0, x0 + cw, sh)
    else:                 # too tall: crop height
        ch = int(sw / target / zoom)
        y0 = int((sh - ch) * 0.5)
        box = (0, y0, sw, y0 + ch)
    im = im.crop(box).resize((tw, th), Image.LANCZOS)
    if boost != 1.0:
        im = ImageEnhance.Color(im).enhance(boost)
    return im


def tag(draw, x, y, label, fnt, bg=INK, fg=WHITE):
    tw = draw.textlength(label, font=fnt)
    pad_x, pad_y = 9, 5
    draw.rectangle([x, y, x + tw + 2 * pad_x, y + fnt.size + 2 * pad_y],
                   fill=bg)
    draw.text((x + pad_x, y + pad_y), label, font=fnt, fill=fg)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")
    MX = 28                      # outer margin
    CW = W - 2 * MX              # 968 content width

    # ---------- 1. Nameplate: dark broadsheet masthead ----------
    d.rectangle([0, 0, W, 116], fill=DARK)
    d.rectangle([0, 116, W, 120], fill=RED)
    f_name = font(F_SERIF_B, 54)
    d.text((MX, 20), "THE WORLD TODAY", font=f_name, fill=WHITE)
    # red LIVE pill, top right
    f_live = font(F_SANS_B, 22)
    pill = "● LIVE"
    pw = d.textlength(pill, font=f_live)
    px = W - MX - pw - 24
    d.rounded_rectangle([px - 12, 20, px + pw + 12, 20 + 40], radius=20,
                        fill=RED)
    d.text((px, 27), pill, font=f_live, fill=WHITE)
    # date sits under the pill, right-aligned; subtitle stays left
    f_date = font(F_SANS_B, 18)
    date_txt = "WEDNESDAY  •  18 NOVEMBER 2026"
    dw = d.textlength(date_txt, font=f_date)
    d.text((W - MX - dw, 74), date_txt, font=f_date, fill=MUTE)
    f_sub = font(F_SERIF, 19)
    d.text((MX, 80), "The world's news in one image", font=f_sub, fill=MUTE)

    # ---------- 2. Breaking banner ----------
    by = 132
    d.rectangle([MX, by, W - MX, by + 40], fill=RED)
    f_brk = font(F_SANS_B, 21)
    d.text((MX + 14, by + 8), "BREAKING", font=f_brk, fill=WHITE)
    bx = MX + 14 + d.textlength("BREAKING", font=f_brk) + 16
    d.line([bx, by + 7, bx, by + 33], fill=WHITE, width=2)
    f_tick = font(F_SANS_B, 20)
    tick = "TRUMP LANDS IN SHENZHEN  —  XI AND PUTIN MEET AHEAD OF TALKS"
    d.text((bx + 14, by + 9), tick, font=f_tick, fill=WHITE)

    # ---------- 3. Lead photo with broadcast lower third ----------
    ly, lh = 184, 316
    lead = fit_cover("assets/shenzhen.jpg", CW, lh, x0_frac=0.52,
                     boost=1.06, zoom=1.45)
    img.paste(lead, (MX, ly))
    d.rectangle([MX, ly, W - MX, ly + 2], fill=RED)
    lt_h = 126
    lt_y = ly + lh - lt_h
    d.rectangle([MX, lt_y, W - MX, ly + lh], fill=(12, 18, 34, 222))
    d.rectangle([MX, lt_y, MX + 6, ly + lh], fill=RED)
    f_kick = font(F_SANS_B, 19)
    d.text((MX + 20, lt_y + 10), "SHENZHEN  •  DIPLOMACY",
           font=f_kick, fill=(255, 92, 92))
    f_head = font(F_SERIF_B, 36)
    d.text((MX + 20, lt_y + 34), "THREE LEADERS, ONE SUMMIT",
           font=f_head, fill=WHITE)
    f_dek = font(F_SANS, 19)
    deck = ("Trump lands in China as Xi and Putin meet a day ahead of the "
            "first US–China–Russia three-way talks.")
    dy = lt_y + 78
    for line in wrap(d, deck, f_dek, CW - 40):
        d.text((MX + 20, dy), line, font=f_dek, fill=(226, 228, 234))
        dy += 23

    # ---------- 4. Two-by-two story cards ----------
    cards = [
        ("assets/kuwait.jpg", 0.30, "THE GULF", "KUWAIT",
         "IRAN HITS KUWAIT, BAHRAIN",
         "Tehran strikes a US base and Gulf sites after US hits on "
         "Qeshm Island.", 1.3),
        ("assets/kerch.jpg", 0.50, "UKRAINE", "KERCH",
         "KERCH BRIDGE HIT AGAIN",
         "Ukraine strikes the Crimean link; part of the road span "
         "collapses.", 1.0),
        ("assets/capitol.jpg", 0.50, "WASHINGTON", "WASHINGTON",
         "DEMOCRATS TAKE SENATE",
         "Peltola unseats Sullivan in Alaska; Democrats lead 56–44.",
         1.0),
        ("assets/gaza.jpg", 0.50, "GAZA", "GAZA CITY",
         "TRUCE AT RISK",
         "The Board of Peace warns the Gaza ceasefire is at risk of "
         "collapse.", 1.0),
    ]
    f_ckick = font(F_SANS_B, 17)
    f_chead = font(F_SANS_B, 25)
    f_cdek = font(F_SANS, 18)
    f_ptag = font(F_SANS_B, 14)
    card_w = (CW - 24) // 2
    card_h = 168
    photo_w = 180
    gx, gy = MX, 520
    for i, (photo, fx, kick, place, head, dek, zm) in enumerate(cards):
        cx = gx + (i % 2) * (card_w + 24)
        cy = gy + (i // 2) * (card_h + 16)
        ph = fit_cover(photo, photo_w, card_h, x0_frac=fx, boost=1.05,
                       zoom=zm)
        img.paste(ph, (cx, cy))
        tag(d, cx, cy + card_h - 26, place, f_ptag)
        tx = cx + photo_w + 14
        tw = card_w - photo_w - 14
        d.text((tx, cy + 2), kick, font=f_ckick, fill=RED)
        hy = cy + 26
        # auto-wrap headline; hard fail if it ever overflows the card
        for line in wrap(d, head, f_chead, tw):
            if d.textlength(line, font=f_chead) > tw:
                raise SystemExit(f"headline overflow: {line!r}")
            d.text((tx, hy), line, font=f_chead, fill=INK)
            hy += 29
        dy = hy + 6
        for line in wrap(d, dek, f_cdek, tw):
            d.text((tx, dy), line, font=f_cdek, fill=(58, 56, 52))
            dy += 23
        if i % 2 == 0:
            d.line([cx + card_w + 12, cy + 6, cx + card_w + 12,
                    cy + card_h - 6], fill=RULE, width=1)

    # ---------- 5. News ticker: the briefs ----------
    ty = 892
    d.rectangle([0, ty, W, ty + 78], fill=DARK)
    d.rectangle([0, ty, W, ty + 3], fill=RED)
    f_tk = font(F_SANS_B, 19)
    f_tb = font(F_SANS, 19)
    lines = [
        [("EBOLA  ", RED), ("DR Congo outbreak passes 11,000 cases",
                             WHITE),
         ("   •   ", (150, 155, 170)),
         ("ANTHROPIC  ", RED),
         ("Record $81.3bn stock offering", WHITE)],
        [("MEASLES  ", RED),
         ("US loses measles-free status after 26 years", WHITE)],
    ]
    ly2 = ty + 14
    for segs in lines:
        total = sum(d.textlength(t, font=f_tk if c is RED else f_tb)
                    for t, c in segs)
        if total > CW:
            raise SystemExit(f"ticker line overflow: {total:.0f} > {CW}")
        x = MX
        for text, col in segs:
            fnt = f_tk if col is RED else f_tb
            d.text((x, ly2), text, font=fnt, fill=col)
            x += d.textlength(text, font=fnt)
        ly2 += 27

    # ---------- 6. Footer: photo credits ----------
    f_ft = font(F_SANS, 13)
    cred = ("Photos: Wikimedia Commons — Shenzhen: Sparktour (CC BY-SA 4.0); "
            "Kuwait Towers: Gladiator2030 (CC BY-SA 4.0); Kerch Bridge: "
            "Alexxx1979 (CC BY-SA 4.0); US Capitol: Noclip (public domain); "
            "Gaza City: OneArmedMan (public domain).")
    fy = 982
    for line in wrap(d, cred, f_ft, CW):
        d.text((MX, fy), line, font=f_ft, fill=GREY)
        fy += 17

    img.save(OUT, optimize=True)
    print(f"wrote {OUT} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()

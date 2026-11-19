#!/usr/bin/env python3
"""Draw entry.png: the world news of Thursday 19 November 2026 in one picture.

A 1024x1024 front-page style card: a dated masthead, six story panels with
flat geometric icons, and a one-line ticker of smaller stories at the foot.
Pure Pillow, no network, no image assets -- every shape is drawn here.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette ---
BG = (10, 26, 48)          # deep navy page
CARD = (20, 42, 76)        # panel card
CARD_EDGE = (44, 76, 128)  # panel outline
INK = (255, 255, 255)      # headline white
SOFT = (185, 201, 228)     # body text, pale blue-grey
GOLD = (255, 201, 77)      # the date, and small highlights
TICKER_BG = (7, 19, 36)
TICKER_INK = (150, 172, 205)

W = H = 1024

FONT_DIR = "/usr/share/fonts/truetype/noto"
BOLD = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")
SEMI = os.path.join(FONT_DIR, "NotoSans-SemiBold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def fit_font(draw, s, path, start, max_w, floor=12):
    """Largest font (<= start) whose single line fits max_w."""
    size = start
    while size > floor:
        f = font(path, size)
        if text_w(draw, s, f) <= max_w:
            return f
        size -= 2
    return font(path, floor)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns the list of lines."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in=None, rot=-90.0):
    """Points of a five-pointed star centred on (cx, cy)."""
    if r_in is None:
        r_in = r_out * 0.42
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36.0)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- stories ---
# (accent colour, icon kind, headline, one-line summary)
STORIES = [
    ((56, 189, 248), "controller",
     "GTA VI LAUNCHES WORLDWIDE",
     "After a 13-year wait, gamers pour into Vice City as the global "
     "rollout begins."),
    ((248, 113, 113), "capitol",
     "JEFFRIES TO LEAD THE US HOUSE",
     "Democrats nominate Hakeem Jeffries, set to be the first "
     "African-American Speaker."),
    ((251, 191, 36), "flags",
     "TRUMP, XI AND PUTIN IN CHINA",
     "The three leaders gather in China; a Trump-Putin one-on-one is "
     "set for Thursday."),
    ((96, 165, 250), "eustars",
     "EU PROPOSES \u20ac45BN LOAN FOR UKRAINE",
     "The loan would be repaid once Russia pays reparations."),
    ((167, 139, 250), "voyager",
     "VOYAGER 1 IS ONE LIGHT-DAY AWAY",
     "NASA's farthest probe, launched in 1977, reaches a full "
     "light-day from Earth."),
    ((52, 211, 153), "scales",
     "WORLD COURT RULES ON MYANMAR",
     "The ICJ delivers its judgment in the Rohingya genocide case "
     "at The Hague."),
]

TICKER = ("ALSO TODAY:  Cyclone Akvan nears India's east coast  \u2022  "
          "A Van Gogh sells for a record $190.4m  \u2022  "
          "Crimean Bridge attacked again")


# ------------------------------------------------------------------- page ---
def new_page():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def draw_masthead(draw):
    """Title, the date in very large type, and a gold rule."""
    f_title = fit_font(draw, "WORLD NEWS IN ONE PICTURE", BOLD, 60, W - 80)
    draw.text((W / 2, 30), "WORLD NEWS IN ONE PICTURE", font=f_title,
              fill=INK, anchor="ma")
    date = "THURSDAY 19 NOVEMBER 2026"
    f_date = fit_font(draw, date, BOLD, 84, W - 64)
    draw.text((W / 2, 104), date, font=f_date, fill=GOLD, anchor="ma")
    draw.line([(40, 196), (W - 40, 196)], fill=GOLD, width=3)


# ------------------------------------------------------------------ icons ---
# Each icon is drawn flat, in its accent colour with white details, inside a
# roughly 100x100 box centred on (cx, cy).

def icon_controller(d, cx, cy, ac):
    d.rounded_rectangle([cx - 47, cy - 27, cx + 47, cy + 27], 26, fill=ac)
    d.rectangle([cx - 35, cy - 4, cx - 17, cy + 4], fill=INK)      # d-pad bar
    d.rectangle([cx - 30, cy - 9, cx - 22, cy + 9], fill=INK)      # d-pad post
    d.ellipse([cx + 12, cy - 15, cx + 25, cy - 2], fill=INK)       # buttons
    d.ellipse([cx + 27, cy - 2, cx + 40, cy + 11], fill=INK)
    d.ellipse([cx - 9, cy + 8, cx - 1, cy + 16], fill=BG)          # sticks
    d.ellipse([cx + 2, cy + 8, cx + 10, cy + 16], fill=BG)


def icon_capitol(d, cx, cy, ac):
    d.pieslice([cx - 29, cy - 36, cx + 29, cy + 8], 180, 360, fill=ac)  # dome
    d.polygon([(cx, cy - 47), (cx, cy - 37), (cx + 11, cy - 42)], fill=GOLD)
    d.line([(cx, cy - 37), (cx, cy - 30)], fill=ac, width=3)
    d.rectangle([cx - 42, cy - 6, cx + 42, cy + 1], fill=ac)       # entablature
    for i in range(4):                                             # columns
        x = cx - 33 + i * 20
        d.rectangle([x, cy + 3, x + 8, cy + 25], fill=INK)
    d.rectangle([cx - 44, cy + 25, cx + 44, cy + 31], fill=ac)     # steps
    d.rectangle([cx - 38, cy + 31, cx + 38, cy + 37], fill=ac)


def icon_flags(d, cx, cy, ac):
    cols = [(248, 113, 113), (96, 165, 250), (251, 191, 36)]
    for i, dx in enumerate((-34, 0, 34)):
        x = cx + dx
        d.line([(x, cy + 38), (x, cy - 36)], fill=INK, width=4)
        d.polygon([(x, cy - 36), (x + 23, cy - 32), (x + 23, cy - 18),
                   (x, cy - 22)], fill=cols[i])
    d.line([(cx - 47, cy + 38), (cx + 47, cy + 38)], fill=INK, width=3)


def icon_eustars(d, cx, cy, ac):
    d.ellipse([cx - 41, cy - 41, cx + 41, cy + 41], outline=ac, width=3)
    for i in range(12):
        a = math.radians(i * 30.0 - 90.0)
        sx, sy = cx + 32 * math.cos(a), cy + 32 * math.sin(a)
        d.polygon(star_points(sx, sy, 6.0), fill=GOLD)
    d.text((cx, cy + 2), "\u20ac", font=font(BOLD, 44), fill=INK, anchor="mm")


def icon_voyager(d, cx, cy, ac):
    d.pieslice([cx - 42, cy - 34, cx - 8, cy + 2], 90, 270, fill=INK)  # dish
    d.line([(cx - 25, cy - 16), (cx - 4, cy - 4)], fill=INK, width=3)  # feed
    d.rectangle([cx - 11, cy - 7, cx + 9, cy + 11], fill=ac)           # bus
    d.line([(cx - 11, cy + 20), (cx - 2, cy + 11)], fill=ac, width=3)  # booms
    d.line([(cx + 9, cy + 20), (cx + 0, cy + 11)], fill=ac, width=3)
    for x0 in (cx - 45, cx + 13):                                      # panels
        d.rectangle([x0, cy + 18, x0 + 30, cy + 33], fill=ac)
        d.line([(x0 + 10, cy + 18), (x0 + 10, cy + 33)], fill=BG, width=2)
        d.line([(x0 + 20, cy + 18), (x0 + 20, cy + 33)], fill=BG, width=2)
    for r in (9, 16, 23):                                              # signal
        d.arc([cx + 4, cy - 16 - r, cx + 4 + 2 * r, cy - 16 + r],
              -55, 45, fill=GOLD, width=3)


def icon_scales(d, cx, cy, ac):
    d.ellipse([cx - 4, cy - 42, cx + 4, cy - 34], fill=ac)         # finial
    d.rectangle([cx - 3, cy - 34, cx + 3, cy + 30], fill=ac)       # post
    d.rectangle([cx - 43, cy - 31, cx + 43, cy - 25], fill=ac)     # beam
    d.ellipse([cx - 5, cy - 33, cx + 5, cy - 23], fill=GOLD)       # pivot
    for sgn in (-1, 1):                                            # pans
        px = cx + sgn * 37
        d.line([(cx + sgn * 40, cy - 25), (px - 11, cy + 0)], fill=INK, width=2)
        d.line([(cx + sgn * 40, cy - 25), (px + 11, cy + 0)], fill=INK, width=2)
        d.pieslice([px - 14, cy - 4, px + 14, cy + 16], 0, 180, fill=ac)
    d.rectangle([cx - 17, cy + 30, cx + 17, cy + 37], fill=ac)     # base


ICONS = {
    "controller": icon_controller,
    "capitol": icon_capitol,
    "flags": icon_flags,
    "eustars": icon_eustars,
    "voyager": icon_voyager,
    "scales": icon_scales,
}


# ----------------------------------------------------------------- panels ---
def draw_panel(d, x, y, w, h, story):
    accent, kind, headline, sub = story
    d.rounded_rectangle([x, y, x + w, y + h], 18, fill=CARD,
                        outline=CARD_EDGE, width=2)
    d.rectangle([x + 16, y, x + w - 16, y + 7], fill=accent)
    ICONS[kind](d, x + 68, y + h // 2 + 4, accent)
    tx, tw = x + 130, w - 130 - 18
    f_head = font(BOLD, 30)
    head_lines = wrap(d, headline, f_head, tw)
    yy = y + 24
    for line in head_lines:
        d.text((tx, yy), line, font=f_head, fill=INK)
        yy += 38
    f_sub = font(REG, 21)
    yy += 8
    for line in wrap(d, sub, f_sub, tw):
        d.text((tx, yy), line, font=f_sub, fill=SOFT)
        yy += 28


def draw_panels(d):
    mx, gap, top, ph = 28, 16, 212, 232
    pw = (W - 2 * mx - gap) // 2
    for i, story in enumerate(STORIES):
        x = mx + (i % 2) * (pw + gap)
        y = top + (i // 2) * (ph + 14)
        draw_panel(d, x, y, pw, ph, story)


def draw_ticker(d):
    d.rectangle([0, 950, W, H], fill=TICKER_BG)
    d.line([(0, 950), (W, 950)], fill=GOLD, width=2)
    f = fit_font(d, TICKER, REG, 23, W - 48)
    d.text((W / 2, 986), TICKER, font=f, fill=TICKER_INK, anchor="mm")


def main():
    img, d = new_page()
    draw_masthead(d)
    draw_panels(d)
    draw_ticker(d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: {img.size[0]}x{img.size[1]}, {size} bytes")
    assert img.size == (1024, 1024), "must be exactly 1024x1024"
    assert size <= 1048576, "must be at most 1 MiB"


if __name__ == "__main__":
    main()

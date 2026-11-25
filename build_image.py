#!/usr/bin/env python3
"""Draw the news-image-20261124 front page and save entry.png.

Fresh build from the prose spec: a newspaper front page summing up
Tuesday 24 November 2026. Run from the repo root:
    python3 build_image.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
RIGHT = W - MARGIN

PAPER = (247, 241, 227)      # warm off-white
INK = (17, 17, 17)           # black ink
RED = (163, 22, 33)          # deep-red accent
NAVY = (27, 42, 74)          # dark-navy panel
NAVY_LIGHT = (58, 74, 110)
GOLD = (217, 165, 33)        # golden scales
GOLD_DARK = (178, 132, 20)
COLUMN = (214, 205, 188)     # courthouse columns
STONE = (235, 229, 214)      # courthouse stone
GREY = (90, 84, 72)          # secondary text

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, size=18):
    fnt = font(SANS_BOLD, size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + size + 6


def headline(draw, x, y, text, size, max_width, leading=None):
    fnt = font(SERIF_BOLD, size)
    leading = leading or int(size * 1.12)
    lines = wrap(draw, text, fnt, max_width)
    return draw_lines(draw, lines, x, y, fnt, INK, leading)


def body(draw, x, y, text, size, max_width, leading=None):
    fnt = font(SERIF, size)
    leading = leading or int(size * 1.28)
    lines = wrap(draw, text, fnt, max_width)
    return draw_lines(draw, lines, x, y, fnt, INK, leading)


def draw_scales(draw, cx, top, bottom):
    """Golden scales of justice centred on cx, spanning top..bottom."""
    mid_y = top + (bottom - top) * 0.42
    # top finial
    draw.ellipse([cx - 6, top - 4, cx + 6, top + 8], fill=GOLD)
    # central pole
    draw.rectangle([cx - 3, top + 4, cx + 3, bottom - 26], fill=GOLD)
    # crossbar
    draw.rectangle([cx - 78, mid_y - 4, cx + 78, mid_y + 4], fill=GOLD)
    draw.ellipse([cx - 84, mid_y - 8, cx - 70, mid_y + 8], fill=GOLD)
    draw.ellipse([cx + 70, mid_y - 8, cx + 84, mid_y + 8], fill=GOLD)
    # hanging chains and pans
    for side in (-1, 1):
        px = cx + side * 78
        draw.line([(px, mid_y + 4), (px - 26, mid_y + 52)], fill=GOLD, width=3)
        draw.line([(px, mid_y + 4), (px + 26, mid_y + 52)], fill=GOLD, width=3)
        draw.line([(px, mid_y + 4), (px, mid_y + 52)], fill=GOLD, width=3)
        draw.pieslice([px - 30, mid_y + 44, px + 30, mid_y + 74],
                      start=0, end=180, fill=GOLD)
        draw.rectangle([px - 30, mid_y + 52, px + 30, mid_y + 58], fill=GOLD)
    # base
    draw.rectangle([cx - 34, bottom - 26, cx + 34, bottom - 18], fill=GOLD)
    draw.rectangle([cx - 44, bottom - 18, cx + 44, bottom - 12], fill=GOLD_DARK)


def draw_gavel(draw, x, y):
    """Small golden gavel, head at (x, y), handle down-right."""
    draw.rectangle([x, y, x + 46, y + 16], fill=GOLD)
    draw.rectangle([x - 4, y - 4, x + 4, y + 20], fill=GOLD_DARK)
    draw.rectangle([x + 42, y - 4, x + 50, y + 20], fill=GOLD_DARK)
    draw.line([(x + 34, y + 14), (x + 62, y + 52)], fill=GOLD, width=7)


def draw_courthouse(draw, x0, y0, x1, y1):
    """Dark-navy panel with a drawn courthouse front and golden scales."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    # faint stars / sky dots
    for sx, sy in [(x0 + 30, y0 + 18), (x1 - 40, y0 + 26), (x0 + 70, y0 + 44),
                   (x1 - 90, y0 + 14), (x0 + 120, y0 + 12)]:
        draw.ellipse([sx, sy, sx + 3, sy + 3], fill=NAVY_LIGHT)
    base_y = y1 - 22
    # steps
    for i, w in enumerate((420, 460, 500)):
        draw.rectangle([x0 + (x1 - x0 - w) // 2, base_y - 6 - i * 7,
                        x0 + (x1 - x0 + w) // 2, base_y + 2 - i * 7],
                       fill=STONE)
    col_top = y0 + 62
    col_bottom = base_y - 20
    # pediment
    mid_x = (x0 + x1) // 2
    draw.polygon([(x0 + 60, col_top), (x1 - 60, col_top),
                  (mid_x, y0 + 14)], fill=STONE)
    draw.ellipse([mid_x - 12, y0 + 30, mid_x + 12, y0 + 54], fill=NAVY)
    # entablature
    draw.rectangle([x0 + 44, col_top, x1 - 44, col_top + 10], fill=STONE)
    # columns
    n_cols = 5
    span = (x1 - 44) - (x0 + 44)
    for i in range(n_cols):
        cx = x0 + 44 + span * (i + 0.5) / n_cols
        draw.rectangle([cx - 13, col_top + 10, cx + 13, col_bottom], fill=COLUMN)
        draw.rectangle([cx - 17, col_top + 10, cx + 17, col_top + 16], fill=STONE)
        draw.rectangle([cx - 17, col_bottom - 6, cx + 17, col_bottom], fill=STONE)
    # doorway between the middle columns
    draw.rectangle([mid_x - 26, col_bottom - 52, mid_x + 26, col_bottom],
                   fill=NAVY)
    # scales of justice in front, centred
    draw_scales(draw, mid_x, y0 + 66, base_y - 8)
    # small gavel at bottom right
    draw_gavel(draw, x1 - 96, y1 - 66)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    y = 14
    mast = font(SERIF_BOLD, 88)
    text = "THE WORLD"
    tw = draw.textlength(text, font=mast)
    draw.text(((W - tw) / 2, y), text, font=mast, fill=INK)
    y += 100

    date_f = font(SERIF_BOLD, 30)
    text = "Tuesday, 24 November 2026"
    tw = draw.textlength(text, font=date_f)
    draw.text(((W - tw) / 2, y), text, font=date_f, fill=INK)
    y += 40

    tag_f = font(SERIF_ITALIC, 20)
    text = "One image. One day. The world in brief."
    tw = draw.textlength(text, font=tag_f)
    draw.text(((W - tw) / 2, y), text, font=tag_f, fill=GREY)
    y += 30

    draw.rectangle([MARGIN, y, RIGHT, y + 4], fill=RED)
    y += 14

    # --- lead row ------------------------------------------------------
    lead_x = MARGIN
    lead_w = 612
    right_x = lead_x + lead_w + 16
    right_w = RIGHT - right_x
    row_top = y

    # illustration panel
    panel_h = 164
    draw_courthouse(draw, lead_x, row_top, lead_x + lead_w, row_top + panel_h)
    y = row_top + panel_h + 10

    y = kicker(draw, lead_x, y, "TECH ON TRIAL", size=19)
    y = headline(draw, lead_x, y,
                 "HUAWEI GUILTY OF TRADE-SECRET THEFT AND BANK FRAUD",
                 size=34, max_width=lead_w)
    y += 4
    y = body(draw, lead_x, y,
             "A US jury convicts Huawei on 10 of 12 counts, including "
             "conspiracy to steal trade secrets and bank fraud, but "
             "acquits it of racketeering. Sentencing is set for "
             "September 2027 and Huawei says it will appeal.",
             size=18, max_width=lead_w)
    lead_bottom = y

    # --- right column: two supporting stories --------------------------
    y = row_top
    y = kicker(draw, right_x, y, "HORMUZ", size=18)
    y = headline(draw, right_x, y,
                 "FOUR TANKERS HIT MINES IN THE STRAIT",
                 size=23, max_width=right_w)
    y += 3
    y = body(draw, right_x, y,
             "Iran says four tankers struck naval mines in the Strait of "
             "Hormuz and caught fire. Tehran orders the strait closed "
             "day by day.",
             size=16, max_width=right_w)
    y += 8
    draw.line([(right_x, y), (RIGHT, y)], fill=(170, 160, 140), width=1)
    y += 10
    y = kicker(draw, right_x, y, "WAR AT SEA", size=18)
    y = headline(draw, right_x, y,
                 "UKRAINE HITS RUSSIAN SHIPS IN TWO SEAS",
                 size=23, max_width=right_w)
    y += 3
    y = body(draw, right_x, y,
             "Ukrainian drones strike a Russian cargo ship in the Gulf of "
             "Finland and a corvette off Libya, which Kyiv says was sunk. "
             "Poland accuses Russia of a new airspace violation.",
             size=16, max_width=right_w)
    right_bottom = y

    y = max(lead_bottom, right_bottom) + 10
    draw.line([(MARGIN, y), (RIGHT, y)], fill=INK, width=2)
    y += 12

    # --- second row: three compact stories ----------------------------
    col_w = (RIGHT - MARGIN - 2 * 20) // 3
    cols = [MARGIN, MARGIN + col_w + 20, MARGIN + 2 * (col_w + 20)]
    stories = [
        ("JUSTICE",
         "WORLD COURT FINDS MYANMAR GUILTY OF GENOCIDE",
         "The UN's highest court rules Myanmar's forces committed "
         "genocide against the Rohingya \u2014 the first such finding "
         "against a state."),
        ("MARKETS",
         "NVIDIA BRINGS BACK JENSEN HUANG",
         "The board reinstates Huang as chief executive after pressure "
         "from President Trump. Shares jump about 30%."),
        ("SPORT",
         "SENEGAL REGAIN AFRICA CUP TITLE",
         "Senegal regain the Africa Cup of Nations title after a sports "
         "court appeal."),
    ]
    row_y = y
    max_y = row_y
    for i, (kick, head, text) in enumerate(stories):
        x = cols[i]
        yy = kicker(draw, x, row_y, kick, size=17)
        yy = headline(draw, x, yy, head, size=21, max_width=col_w)
        yy += 3
        yy = body(draw, x, yy, text, size=15, max_width=col_w)
        max_y = max(max_y, yy)
        if i < 2:
            draw.line([(x + col_w + 10, row_y),
                       (x + col_w + 10, max_y)], fill=(170, 160, 140), width=1)

    y = max_y + 10
    draw.line([(MARGIN, y), (RIGHT, y)], fill=INK, width=2)
    y += 12

    # --- markets strip ---------------------------------------------------
    strip_top = y
    draw.rectangle([MARGIN, strip_top, RIGHT, strip_top + 60], fill=(238, 230, 212))
    draw.rectangle([MARGIN, strip_top, MARGIN + 6, strip_top + 60], fill=RED)
    my = strip_top + 7
    my = headline(draw, MARGIN + 18, my,
                  "WALL STREET'S BEST DAY IN OVER A YEAR",
                  size=20, max_width=RIGHT - MARGIN - 18)
    body(draw, MARGIN + 18, my,
         "Nvidia surges on Huang's return; Sanofi agrees to buy Insmed "
         "for $41bn.",
         size=16, max_width=RIGHT - MARGIN - 18)
    y = strip_top + 60 + 10
    draw.line([(MARGIN, y), (RIGHT, y)], fill=INK, width=2)
    y += 8

    # --- IN BRIEF ---------------------------------------------------------
    y = kicker(draw, MARGIN, y, "IN BRIEF", size=18)
    brief_left = [
        "Turkish military helicopter crash kills five near Eskisehir",
        "Gunmen hold 25 hostage at a Cartagena supermarket",
        "Suspected drone strike hits Riyadh's PIF tower, 11 wounded",
        "Indonesia names two candidates to replace Vice President Gibran",
    ]
    brief_right = [
        "US loses measles elimination status after 25 years",
        "Gaza issues meningitis epidemic alert",
        "Hasina plans return to Bangladesh on 16 December",
        "Hanoi restaurant blast kills at least six",
    ]
    brief_f = font(SANS, 14)
    brief_lead = 19
    by = y
    for item in brief_left:
        draw.text((MARGIN, by), "\u2022  " + item, font=brief_f, fill=INK)
        by += brief_lead
    by = y
    half = MARGIN + (RIGHT - MARGIN) // 2
    for item in brief_right:
        draw.text((half, by), "\u2022  " + item, font=brief_f, fill=INK)
        by += brief_lead
    y = max(by, y + 4 * brief_lead) + 6
    draw.line([(MARGIN, y), (RIGHT, y)], fill=INK, width=2)
    y += 8

    # --- footer ------------------------------------------------------------
    foot_f = font(SERIF_ITALIC, 15)
    text = "All stories first reported Tuesday 24 November 2026."
    tw = draw.textlength(text, font=foot_f)
    draw.text(((W - tw) / 2, y), text, font=foot_f, fill=GREY)
    y += 22
    assert y <= H, f"layout overflow: bottom y={y}"

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

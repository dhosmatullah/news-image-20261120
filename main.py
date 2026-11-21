#!/usr/bin/env python3
"""news-image-20261120: sums up the world news of Friday 20 November 2026
in one 1024x1024 front-page style image, drawn procedurally with the
Python standard library only (no network, no third-party packages).

Writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png locally).
Deterministic: two runs produce identical bytes.
"""
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font
# 5x7 bitmap glyphs, rows top->bottom, '1' = ink. Uppercase set + digits.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "01010", "00100", "00100", "00100", "01010", "10001"),
    "Y": ("10001", "01010", "00100", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "•": ("00000", "00000", "01110", "01110", "01110", "00000", "00000"),
}

# ---------------------------------------------------------------- canvas
PX = bytearray(W * H * 3)


def put(x, y, rgb):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        PX[i] = rgb[0]
        PX[i + 1] = rgb[1]
        PX[i + 2] = rgb[2]


def rect(x, y, w, h, rgb):
    for yy in range(y, y + h):
        if 0 <= yy < H:
            base = yy * W * 3
            for xx in range(max(0, x), min(W, x + w)):
                i = base + xx * 3
                PX[i] = rgb[0]
                PX[i + 1] = rgb[1]
                PX[i + 2] = rgb[2]


def line(x0, y0, x1, y1, rgb, thick=1):
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    r = thick // 2
    for s in range(steps + 1):
        x = x0 + (x1 - x0) * s // steps
        y = y0 + (y1 - y0) * s // steps
        rect(x - r, y - r, thick, thick, rgb)


def circle(cx, cy, rad, rgb):
    for yy in range(cy - rad, cy + rad + 1):
        for xx in range(cx - rad, cx + rad + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= rad * rad:
                put(xx, yy, rgb)


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def text(x, y, s, scale, rgb, center_in=None):
    if center_in is not None:
        x = center_in[0] + (center_in[1] - center_in[0] - text_w(s, scale)) // 2
    cx = x
    for ch in s.upper():
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    rect(cx + col * scale, y + row * scale, scale, scale, rgb)
        cx += 6 * scale
    return cx


def burst(cx, cy, r_out, r_in, rgb):
    import math

    for k in range(16):
        ang = math.pi * k / 8.0
        x1 = int(cx + r_in * math.cos(ang))
        y1 = int(cy + r_in * math.sin(ang))
        x2 = int(cx + r_out * math.cos(ang))
        y2 = int(cy + r_out * math.sin(ang))
        line(cx, cy, x2, y2, rgb, 3)
        line(x1, y1, x2, y2, rgb, 3)
    circle(cx, cy, r_in, rgb)


# ---------------------------------------------------------------- palette
PAPER = (242, 236, 223)
NAVY = (16, 29, 51)
NAVY2 = (27, 42, 74)
RED = (193, 18, 31)
GOLD = (232, 183, 75)
WHITE = (255, 255, 255)
INK = (24, 26, 32)
GRAY = (96, 98, 104)
CARD = (255, 253, 247)
ORANGE = (255, 122, 26)
YELLOW = (255, 209, 26)
GREEN = (18, 84, 52)
SKY = (13, 22, 44)


# ---------------------------------------------------------------- scenes
def masthead():
    rect(0, 0, W, H, PAPER)
    rect(0, 0, W, 148, NAVY)
    text(0, 14, "THE WORLD IN ONE DAY", 3, GOLD, center_in=(0, W))
    text(0, 44, "20 NOVEMBER 2026", 10, WHITE, center_in=(0, W))
    text(0, 122, "FRIDAY - WORLD NEWS SUMMARY", 2, (178, 190, 214),
         center_in=(0, W))
    rect(0, 148, W, 8, RED)


def hero():
    x0, y0, x1, y1 = 24, 172, 1000, 516
    rect(x0, y0, x1 - x0, y1 - y0, SKY)
    # stars
    for sx, sy in ((80, 200), (210, 186), (330, 214), (470, 190), (600, 208),
                   (720, 184), (860, 200), (940, 226), (150, 240), (540, 232)):
        rect(sx, sy, 3, 3, (150, 165, 200))
    # missile trails, kept in the lower-right so they clear the headline
    for tx, ty, hx, hy in ((988, 336, 862, 442), (946, 318, 782, 436),
                           (992, 392, 902, 448)):
        line(tx, ty, hx, hy, (120, 70, 40), 5)
        line(tx, ty, hx, hy, ORANGE, 2)
        circle(tx, ty, 5, YELLOW)
        burst(hx, hy, 24, 8, ORANGE)
        burst(hx, hy, 15, 5, YELLOW)
    # drones (small X silhouettes) in the kicker row, right of the label
    for dx, dy in ((520, 204), (668, 198), (806, 206)):
        line(dx - 16, dy - 10, dx + 16, dy + 10, (6, 8, 14), 5)
        line(dx - 16, dy + 10, dx + 16, dy - 10, (6, 8, 14), 5)
        circle(dx, dy, 5, (6, 8, 14))
    # skyline silhouette with lit windows
    base = 470
    towers = ((24, 392, 74, 78), (104, 356, 62, 114), (172, 402, 84, 68),
              (262, 372, 56, 98), (640, 388, 70, 82), (716, 348, 60, 122),
              (782, 398, 88, 72), (876, 366, 64, 104), (946, 404, 54, 66))
    for tx, ty, tw, th in towers:
        rect(tx, ty, tw, th, (5, 7, 12))
        for wy in range(ty + 10, base - 8, 16):
            for wx in range(tx + 8, tx + tw - 8, 14):
                if (wx * 7 + wy * 13) % 5 < 2:
                    rect(wx, wy, 5, 7, (255, 196, 64))
    rect(x0, base, x1 - x0, y1 - base, (5, 7, 12))
    # headline block
    text(44, 196, "UKRAINE WAR", 3, RED)
    text(44, 226, "RUSSIA FIRES 400+ DRONES", 6, WHITE)
    text(44, 276, "& 110 MISSILES AT UKRAINE", 6, WHITE)
    text(44, 330, "KYIV BRIDGES & POWER HIT - 8 KILLED", 3, GOLD)
    text(44, 358, "MISSILES FALL INSIDE POLAND (NATO)", 3, GOLD)


def panel(x, y, w, h, accent, kicker, head1, head2, sub1, sub2, icon):
    rect(x, y, w, h, CARD)
    rect(x, y, w, 8, accent)
    rect(x, y, w, 2, accent)
    rect(x, y + h - 2, w, 2, accent)
    rect(x, y, 2, h, accent)
    rect(x + w - 2, y, 2, h, accent)
    text(x + 18, y + 18, kicker, 2, accent)
    text(x + 18, y + 42, head1, 3, INK)
    text(x + 18, y + 72, head2, 3, INK)
    text(x + 18, y + 106, sub1, 2, GRAY)
    text(x + 18, y + 124, sub2, 2, GRAY)
    icon(x + w - 108, y + 30)


def icon_flags(cx, cy):
    # three mini flags: USA, China, Russia
    flags = []
    for i in range(3):
        fx = cx + i * 34
        flags.append(fx)
        rect(fx, cy, 30, 44, WHITE)
    # USA: stripes + blue canton
    for r in range(6):
        rect(flags[0], cy + r * 7 + (2 if r else 0), 30, 4, (178, 34, 52))
    rect(flags[0], cy, 14, 20, (60, 59, 110))
    for r in range(3):
        for c in range(3):
            rect(flags[0] + 2 + c * 4, cy + 3 + r * 6, 2, 2, WHITE)
    # China: red + yellow stars
    rect(flags[1], cy, 30, 44, (222, 41, 16))
    rect(flags[1] + 4, cy + 5, 6, 6, (255, 222, 0))
    for dx, dy in ((14, 4), (16, 10), (14, 16)):
        rect(flags[1] + dx, cy + dy, 3, 3, (255, 222, 0))
    # Russia: white / blue / red bands
    rect(flags[2], cy, 30, 15, WHITE)
    rect(flags[2], cy + 15, 30, 14, (0, 57, 166))
    rect(flags[2], cy + 29, 30, 15, (213, 43, 30))
    rect(cx, cy + 52, 96, 4, GOLD)


def icon_scales(cx, cy):
    c = (146, 110, 30)
    rect(cx + 44, cy + 6, 6, 62, c)
    rect(cx + 10, cy + 10, 74, 5, c)
    circle(cx + 47, cy + 4, 6, c)
    for px in (cx + 12, cx + 82):
        line(px, cy + 15, px - 10, cy + 44, c, 3)
        line(px, cy + 15, px + 10, cy + 44, c, 3)
        line(px - 12, cy + 44, px + 12, cy + 44, c, 4)
    rect(cx + 30, cy + 68, 34, 5, c)


def icon_chart(cx, cy):
    line(cx + 6, cy + 70, cx + 92, cy + 70, GRAY, 3)
    line(cx + 6, cy + 70, cx + 6, cy + 4, GRAY, 3)
    bars = ((16, 52, 18), (38, 38, 32), (60, 22, 48))
    for bx, bt, bh in bars:
        rect(cx + bx, cy + 70 - bh, 16, bh, (31, 122, 76))
    line(cx + 12, cy + 44, cx + 44, cy + 28, RED, 4)
    line(cx + 44, cy + 28, cx + 84, cy + 8, RED, 4)
    line(cx + 84, cy + 8, cx + 70, cy + 8, RED, 4)
    line(cx + 84, cy + 8, cx + 84, cy + 22, RED, 4)


def icon_eu_uk(cx, cy):
    import math

    # UK flag as a rectangle: navy field, white cross, red cross
    rect(cx, cy + 8, 52, 40, (1, 33, 105))
    rect(cx + 21, cy + 8, 10, 40, WHITE)
    rect(cx, cy + 23, 52, 10, WHITE)
    rect(cx + 23, cy + 8, 6, 40, RED)
    rect(cx, cy + 25, 52, 6, RED)
    # EU circle overlapping it: blue disc, ring of yellow stars
    circle(cx + 72, cy + 28, 26, (0, 51, 153))
    for k in range(12):
        ang = 2 * math.pi * k / 12.0
        sx = int(cx + 72 + 18 * math.cos(ang))
        sy = int(cy + 28 + 18 * math.sin(ang))
        rect(sx - 2, sy - 2, 4, 4, (255, 204, 0))


def grid_panels():
    pw, ph = 476, 150
    panel(24, 532, pw, ph, (146, 30, 30), "SHENZHEN SUMMIT",
          "TRUMP, XI & PUTIN", "MEET FACE TO FACE",
          "JOINT PLEDGE: NO NUCLEAR WAR", "BUT NO ARMS DEAL REACHED",
          icon_flags)
    panel(524, 532, pw, ph, (146, 110, 30), "THE HAGUE - WORLD COURT",
          "MYANMAR GUILTY OF", "ROHINGYA GENOCIDE",
          "ICJ RULES ON 2017 CRIMES", "REPARATIONS ORDERED",
          icon_scales)
    panel(24, 698, pw, ph, (31, 122, 76), "TECH - MARKETS",
          "ANTHROPIC $81BN", "RECORD IPO",
          "BIGGEST STOCK DEBUT EVER", "AI BOOM PEAKS ON NASDAQ",
          icon_chart)
    panel(524, 698, pw, ph, (0, 51, 153), "BRUSSELS SUMMIT",
          "UK & EU STRIKE", "RESET DEAL",
          "100K YOUTH VISAS A YEAR", "FOOD TRADE & CARBON PACT",
          icon_eu_uk)


def bottom_bands():
    rect(24, 864, 976, 62, GREEN)
    text(0, 876, "COP31 ANTALYA: FINAL DAY, NO DEAL", 3, WHITE,
         center_in=(0, W))
    text(0, 902, "FOSSIL-FUEL PLEDGE DROPPED FROM DRAFT", 2, (190, 230, 200),
         center_in=(0, W))
    rect(24, 938, 976, 44, NAVY)
    text(0, 946, "ALSO: HAITI POLICE KILL 34 GANG MEMBERS", 2, WHITE,
         center_in=(0, W))
    text(0, 964, "CYCLONE AKVAN HITS ODISHA - IRAQ FORCES ENTER JURF AL-SAKHAR",
         2, (178, 190, 214), center_in=(0, W))
    text(0, 994, "SOURCES: REUTERS - AP - BBC - OPEN CHRONICLE - PANA", 2,
         GRAY, center_in=(0, W))


# ---------------------------------------------------------------- png out
def save_png(path):
    raw = bytearray()
    row_bytes = W * 3
    for y in range(H):
        raw.append(0)
        raw += PX[y * row_bytes:(y + 1) * row_bytes]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    masthead()
    hero()
    grid_panels()
    bottom_bands()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    size = save_png(os.path.join(out_dir, "entry.png"))
    print(f"wrote entry.png {size} bytes {W}x{H}")


if __name__ == "__main__":
    main()

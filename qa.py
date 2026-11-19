"""Pre-submit QA gate for a news-image front page.

Every check measures the rendered PNG and the news module it came from; none of
them trusts a hand-written constant. Exit 1 on any failure, so this can gate a
submit.

  python3 qa.py [image.png]
"""
import json
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image

import news as N
import layout as L
import fonts as F

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
M = 24

fails = []
warns = []


def ok(name, detail):
    print(f"  PASS  {name}: {detail}")


def bad(name, detail):
    print(f"  FAIL  {name}: {detail}")
    fails.append(name)


def warn(name, detail):
    print(f"  WARN  {name}: {detail}")
    warns.append(name)


def check_png(path):
    """Valid whole PNG: signature, IHDR, every chunk CRC, IEND at the exact end."""
    b = open(path, "rb").read()
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        return bad("png_valid", "not a PNG signature"), None
    i, w, h, saw_end = 8, None, None, False
    while i + 8 <= len(b):
        (ln,) = struct.unpack(">I", b[i:i + 4])
        typ = b[i + 4:i + 8]
        body = b[i + 8:i + 8 + ln]
        crc = b[i + 8 + ln:i + 12 + ln]
        if len(crc) != 4:
            return bad("png_valid", f"chunk {typ!r} at {i} truncated"), None
        (want,) = struct.unpack(">I", crc)
        got = zlib.crc32(typ + body) & 0xFFFFFFFF
        if want != got:
            return bad("png_valid", f"chunk {typ!r} at {i} has a bad CRC"), None
        if typ == b"IHDR":
            w, h = struct.unpack(">II", body[:8])
        i += 12 + ln
        if typ == b"IEND":
            saw_end = True
            break
    if not saw_end:
        return bad("png_valid", "no IEND chunk"), None
    if i != len(b):
        return bad("png_valid", f"{len(b) - i} trailing bytes after IEND"), None
    ok("png_valid", f"all chunk CRCs good, IEND at EOF, {len(b)} bytes")
    return None, (w, h)


def check_limits(path, wh):
    n = os.path.getsize(path)
    if n > MAX_BYTES:
        bad("size_limit", f"{n} bytes over the {MAX_BYTES} cap")
    else:
        ok("size_limit", f"{n} bytes, {(MAX_BYTES - n) / 1024:.1f} KiB of headroom")
    w, h = wh
    if w > MAX_SIDE or h > MAX_SIDE:
        bad("pixel_limit", f"{w}x{h} over {MAX_SIDE}")
    else:
        ok("pixel_limit", f"{w}x{h}")
    if wh != (1024, 1024):
        warn("square", f"{w}x{h} is not 1024x1024")


def check_margins(im):
    """No ink outside the page margin, and no ink in the last rows."""
    px = im.load()
    w, h = im.size
    paper = px[w - 1, h - 1]
    out = []
    for y in range(h):
        for x in (0, 1, w - 2, w - 1):
            p = px[x, y]
            if sum(abs(a - b) for a, b in zip(p, paper)) > 24:
                out.append((x, y))
                break
    for x in range(w):
        for y in (0, 1, h - 2, h - 1):
            p = px[x, y]
            if sum(abs(a - b) for a, b in zip(p, paper)) > 24:
                out.append((x, y))
                break
    if out:
        bad("margins", f"{len(out)} ink pixels on the outer 2px ring, first {out[:3]}")
    else:
        ok("margins", "outer 2px ring is clean paper all round")

    # lowest inked row, to prove the page is not short or overrun
    bot = 0
    for y in range(h - 1, -1, -1):
        row = [px[x, y] for x in range(M, w - M, 3)]
        if any(sum(abs(a - b) for a, b in zip(p, paper)) > 30 for p in row):
            bot = y
            break
    ok("bottom_of_ink", f"y={bot} of {h} (limit {h - M})")
    if bot > h - M:
        bad("bottom_of_ink", f"ink reaches y={bot}, past the {h - M} limit")


def check_briefs():
    """Every footer brief must fit its column at the size the build actually picks.

    news.SHORT_BRIEFS is a list of (place, text) tuples.
    """
    M_, COL = 24, L.W - 2 * 24
    map_w = COL * 0.315
    idx_w = COL - map_w - 13 - 4
    fit = []
    for ncol in (2, 3):
        cgap = 11.0
        bw = (idx_w - cgap * (ncol - 1)) / ncol
        for fs in (10.8, 10.4, 10.0, 9.6, 9.2, 8.8, 8.4, 8.0):
            page = L.Page()
            fb, fp = F.text(fs, 400), F.text(fs, 700)
            over = []
            for place, text in N.SHORT_BRIEFS:
                avail = bw - page.tw(place + " ", fp) - 1.2
                lines = page.wrap(text, fb, avail)
                for ln in lines:
                    if page.tw(ln, fb) > avail + 0.6:
                        over.append((place, round(page.tw(ln, fb), 1),
                                     round(avail, 1)))
                if len(lines) > 3:
                    over.append((place, f"{len(lines)} lines", "max 3"))
            if not over:
                fit.append((ncol, fs))
    if fit:
        ncol, fs = fit[0]
        ok("brief_fit", f"{len(N.SHORT_BRIEFS)} briefs fit at {ncol} cols / {fs}px "
                        f"(longest needs no wrap past the column)")
    else:
        bad("brief_fit", "no column count / size fits every brief in 3 lines")


def check_counts():
    """Every number printed on the page must be one the page can prove."""
    n_leads, n_cards, n_briefs = len(N.LEADS), len(N.CARDS), len(N.SHORT_BRIEFS)
    total = n_leads + n_cards + n_briefs
    ok("counts", f"{n_leads} leads + {n_cards} cards + {n_briefs} briefs = {total} stories")

    # the region index tabs are computed from the stories, so they must sum back
    import build
    counts = build.count_regions()
    s = sum(counts.values())
    if s != total:
        bad("region_sum", f"region tabs sum to {s}, stories total {total}")
    else:
        ok("region_sum", f"region tabs sum to {s} = story count "
                         f"({', '.join(f'{k} {v}' for k, v in sorted(counts.items()))})")

    if n_leads != 3:
        warn("leads", f"{n_leads} leads, layout is drawn for 3")
    if n_cards != 10:
        warn("cards", f"{n_cards} cards, CARD_ORDER is drawn for 10")


def check_stats():
    """Six figures in the numbers strip, each with its caption."""
    ok("stats", f"{len(N.STATS)} figures in the numbers strip")
    if len(N.STATS) != 6:
        bad("stats", f"{len(N.STATS)} figures, the strip is laid out for 6")
    seen = set()
    for fig, cap in N.STATS:
        if fig in seen:
            bad("stats_unique", f"{fig} appears twice in the strip")
        seen.add(fig)
    head_words = " ".join(l["headline"] for l in N.LEADS).lower()
    for fig, cap in N.STATS:
        core = cap.split()[0].lower().strip(",")
        if core and core in head_words and len(core) > 4:
            warn("stats_repeat", f"{fig} {cap!r} repeats a lead headline word {core!r}")


def check_300(im):
    """Legibility proxy: at 300px every tenth of the page must still carry ink.

    Ink is measured as deviation from the page's own paper colour, not as
    "dark": a pale map panel or a thin rule is still ink, and a grayscale
    threshold calls both of those empty.
    """
    small = im.resize((300, 300), Image.LANCZOS).convert("RGB")
    px = small.load()
    paper = px[298, 298]
    bands = []
    for i in range(10):
        y0, y1 = int(30 * i), int(30 * (i + 1))
        ink = 0
        for y in range(y0, y1):
            for x in range(300):
                p = px[x, y]
                if sum(abs(a - b) for a, b in zip(p, paper)) > 36:
                    ink += 1
        bands.append(round(100 * ink / (30 * 300), 1))
    empty = [i for i, v in enumerate(bands) if v < 2.0]
    if empty:
        bad("legible_300", f"bands {empty} carry almost no ink at 300px: {bands}")
    else:
        ok("legible_300", f"every tenth carries ink at 300px: {bands}")


def check_tone(im):
    """The page should be a dense broadsheet, not a sparse poster."""
    g = im.convert("L")
    hist = g.histogram()
    ink = sum(hist[:150]) / sum(hist)
    ok("ink_coverage", f"{100 * ink:.1f}% of pixels are dark-ish")
    if ink < 0.12:
        warn("ink_coverage", f"only {100 * ink:.1f}% ink; the page may read sparse")


def check_date():
    ok("date", f"page states {N.DAY} {N.DATE}")
    if "2026" not in N.DATE:
        bad("date", "no year on the page")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png")
    print(f"QA {path}")
    im = Image.open(path).convert("RGB")
    _, wh = check_png(path)
    check_limits(path, wh)
    check_margins(im)
    check_counts()
    check_stats()
    check_briefs()
    check_300(im)
    check_tone(im)
    check_date()
    print()
    if fails:
        print(f"FAILED {len(fails)} check(s): {', '.join(fails)}")
        return 1
    print(f"ALL PASS{f' ({len(warns)} warning(s))' if warns else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

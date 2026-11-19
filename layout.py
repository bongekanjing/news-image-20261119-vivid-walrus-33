"""Draws the front page: one 1024x1024 PNG summing up Wednesday 18 November 2026.

Zones, top to bottom: strap and masthead date, a colour-coded region index with
story counts, "the day in numbers", three lead cards, ten cards in two bands of
five, a locator map beside the briefs, and a date-check footer.

Drawn at SS times final size and box-reduced once, so hairlines and small caps
survive at 1024 and the headlines still carry at 300.
"""
import json
import os

from PIL import Image, ImageDraw

import fonts as F
import news as N

SS = 2
W = H = 1024
S = W * SS

HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (247, 243, 234)
INK = (24, 21, 18)
GREY = (106, 99, 90)
FAINT = (188, 180, 168)
RED = (163, 34, 34)

REGION_COLOUR = {
    "EUROPE": (172, 58, 42),
    "MIDDLE EAST": (176, 126, 26),
    "ASIA": (36, 92, 122),
    "AFRICA": (116, 92, 40),
    "AMERICAS": (46, 74, 126),
    "OCEANIA": (32, 112, 96),
    "WORLD": (88, 84, 80),
    "US": (46, 74, 126),
}
REGION_ORDER = ["EUROPE", "AMERICAS", "ASIA", "MIDDLE EAST", "AFRICA", "OCEANIA", "WORLD"]

M = 26              # page margin, final px


class Page:
    ss = SS

    def __init__(self):
        self.im = Image.new("RGB", (S, S), PAPER)
        self.d = ImageDraw.Draw(self.im)
        self.warn = []

    # ---- primitives, all in final-pixel coordinates ------------------------
    def rect(self, x, y, w, h, col, outline=None, ow=1):
        box = [x * SS, y * SS, (x + w) * SS - 1, (y + h) * SS - 1]
        if outline:
            self.d.rectangle(box, fill=col, outline=outline, width=max(1, int(ow * SS)))
        else:
            self.d.rectangle(box, fill=col)

    def hline(self, x0, y, x1, col=FAINT, t=1.0):
        self.d.rectangle([x0 * SS, int(y * SS), x1 * SS, int(y * SS + max(1, t * SS)) - 1], fill=col)

    def vline(self, x, y0, y1, col=FAINT, t=1.0):
        if y1 <= y0:
            return
        self.d.rectangle([int(x * SS), int(y0 * SS), int(x * SS + max(1, t * SS)) - 1,
                          int(y1 * SS)], fill=col)

    def tw(self, s, font):
        return self.d.textlength(s, font=font) / SS

    def text(self, x, y, s, font, col=INK, track=0.0, anchor="la"):
        """Draw text at final coords; track adds letter-spacing in final px."""
        if not s:
            return 0
        if track == 0:
            self.d.text((x * SS, y * SS), s, font=font, fill=col, anchor=anchor)
            return self.tw(s, font)
        cx = x
        for ch in s:
            self.d.text((cx * SS, y * SS), ch, font=font, fill=col, anchor=anchor)
            cx += self.tw(ch, font) + track
        return cx - x - track

    def wrap(self, s, font, maxw):
        words, lines, cur = s.split(), [], ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if self.tw(t, font) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, font, maxw, leading, col=INK, maxlines=None, ell=None):
        lines = self.wrap(s, font, maxw)
        if maxlines and len(lines) > maxlines:
            lines = lines[:maxlines]
            lines[-1] = ell if ell else lines[-1].rstrip(",;: ") + "\u2026"
        for ln in lines:
            self.text(x, y, ln, font, col)
            y += leading
        return y

    def fit(self, s, fontfn, maxw, start, lo=6):
        """Largest size from `start` down at which `s` fits `maxw` on one line."""
        size = start
        while size > lo:
            f = fontfn(size)
            if self.tw(s, f) <= maxw:
                return f, size
            size -= 1
        return fontfn(lo), lo

    def fit_lines(self, s, maxw, start, lo, nlines=3):
        """Largest size at which `s` wraps to at most `nlines` lines of `maxw`."""
        size = start
        while size > lo:
            f = F.serif(size, 700)
            if len(self.wrap(s, f, maxw)) <= nlines:
                return f, size
            size -= 1
        return F.serif(lo, 700), lo

    def save(self, path):
        out = self.im.resize((W, H), Image.LANCZOS)
        out.save(path, optimize=True)
        return out


def region_of(r):
    return r.split("\u00b7")[0].strip().upper()


def col_for(r):
    return REGION_COLOUR.get(region_of(r), REGION_COLOUR["WORLD"])

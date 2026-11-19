"""Illustrations: flat vector art drawn with PIL, one grammar for the whole page.

Each function draws into a box (x, y, w, h) at final-pixel coordinates and knows
nothing about text except the short tags it is told to set. They are emblems and
diagrams, not photographs: flat fills, one accent colour, no gradient noise.
"""
import math

INK = (26, 23, 20)
WHITE = (250, 248, 243)
PAPER = (247, 243, 234)


def _shade(col, k):
    return tuple(max(0, min(255, int(c * k))) for c in col)


def _tint(col, k):
    return tuple(int(247 + (col[i] - 247) * k) for i in range(3))


class Art:
    def __init__(self, page, x, y, w, h, accent):
        self.p = page
        self.x, self.y, self.w, self.h = x, y, w, h
        self.acc = accent
        self.d = page.d
        self.ss = page.ss

    def box(self, col):
        self.p.rect(self.x, self.y, self.w, self.h, col)

    def rect(self, fx, fy, fw, fh, col):
        self.p.rect(self.x + fx * self.w, self.y + fy * self.h,
                    fw * self.w, fh * self.h, col)

    def circle(self, fx, fy, r, col):
        cx, cy = self.x + fx * self.w, self.y + fy * self.h
        rr = r * min(self.w, self.h)
        self.d.ellipse([(cx - rr) * self.ss, (cy - rr) * self.ss,
                        (cx + rr) * self.ss, (cy + rr) * self.ss], fill=col)

    def poly(self, pts, col):
        pp = [((self.x + a * self.w) * self.ss, (self.y + b * self.h) * self.ss) for a, b in pts]
        self.d.polygon(pp, fill=col)

    def line(self, pts, col, t=1.0):
        pp = [((self.x + a * self.w) * self.ss, (self.y + b * self.h) * self.ss) for a, b in pts]
        self.d.line(pp, fill=col, width=max(1, int(t * self.ss)), joint="curve")

    def arc(self, fx, fy, r, a0, a1, col, t=1.0):
        cx, cy = self.x + fx * self.w, self.y + fy * self.h
        rr = r * min(self.w, self.h)
        self.d.arc([(cx - rr) * self.ss, (cy - rr) * self.ss,
                    (cx + rr) * self.ss, (cy + rr) * self.ss],
                   a0, a1, fill=col, width=max(1, int(t * self.ss)))

    def chip(self, text, x=None, y=0.045, size=0.148, col=INK):
        """A figure reversed out of a solid tag, so the number survives at 300px."""
        from fonts import caps as _caps
        h = size * self.h
        fs = max(4.8, h * 0.64)
        # fit the tag inside 88% of the art, never letting it touch the edges
        for _ in range(14):
            f = _caps(fs, 700)
            tw = self.p.tw(text, f) + max(0.0, (len(text) - 1) * fs * 0.045)
            pad = h * 0.40
            bw = tw + 2 * pad
            if bw <= 0.88 * self.w or fs <= 4.8:
                break
            fs *= 0.92
        if x is None:
            x = 1.0 - (bw / self.w) - 0.035
        bx, by = self.x + x * self.w, self.y + y * self.h
        self.d.rectangle([bx * self.ss, by * self.ss,
                          (bx + bw) * self.ss, (by + h) * self.ss], fill=col)
        self.p.text(bx + pad, by + h * 0.19, text, f, WHITE, track=fs * 0.045)

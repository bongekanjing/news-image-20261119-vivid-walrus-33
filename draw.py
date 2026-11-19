"""Flat raster drawing kit: canvas, stroke font, shapes, PNG writer.

Everything is drawn at SS times the final size and box-filtered down, which
gives clean anti-aliased edges without any third-party library.

Colour is a 3-tuple of ints. Coordinates are in OUTPUT pixels.
"""

import zlib
import struct

SS = 2  # supersample factor


# --------------------------------------------------------------------------
# canvas
# --------------------------------------------------------------------------

class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.W = w * SS
        self.H = h * SS
        self.buf = bytearray(bytes(bg) * (self.W * self.H))

    # -- low level ---------------------------------------------------------
    def _rowspan(self, y, x0, x1, color):
        if y < 0 or y >= self.H:
            return
        if x0 < 0:
            x0 = 0
        if x1 > self.W:
            x1 = self.W
        if x1 <= x0:
            return
        i = (y * self.W + x0) * 3
        self.buf[i:i + (x1 - x0) * 3] = bytes(color) * (x1 - x0)

    def rect(self, x, y, w, h, color):
        X = int(round(x * SS))
        Y = int(round(y * SS))
        W = int(round(w * SS))
        H = int(round(h * SS))
        if W <= 0 or H <= 0:
            return
        for yy in range(Y, Y + H):
            self._rowspan(yy, X, X + W, color)

    def hline(self, x, y, w, thick, color):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, thick, color):
        self.rect(x, y, thick, h, color)

    def frame(self, x, y, w, h, thick, color):
        self.rect(x, y, w, thick, color)
        self.rect(x, y + h - thick, w, thick, color)
        self.rect(x, y, thick, h, color)
        self.rect(x + w - thick, y, thick, h, color)

    def poly(self, pts, color):
        """Fill a polygon (nonzero-free, even-odd) given in output pixels."""
        P = [(x * SS, y * SS) for (x, y) in pts]
        if len(P) < 3:
            return
        ys = [p[1] for p in P]
        y0 = max(0, int(min(ys)))
        y1 = min(self.H - 1, int(max(ys) + 0.999))
        n = len(P)
        for yy in range(y0, y1 + 1):
            sy = yy + 0.5
            xs = []
            for i in range(n):
                ax, ay = P[i]
                bx, by = P[(i + 1) % n]
                if ay == by:
                    continue
                if (ay <= sy < by) or (by <= sy < ay):
                    t = (sy - ay) / (by - ay)
                    xs.append(ax + t * (bx - ax))
            if len(xs) < 2:
                continue
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self._rowspan(yy, int(xs[i] + 0.5), int(xs[i + 1] + 0.5), color)

    def circle(self, cx, cy, r, color):
        pts = []
        for i in range(24):
            a = 6.283185307179586 * i / 24.0
            pts.append((cx + r * _cos(a), cy + r * _sin(a)))
        self.poly(pts, color)

    def ring(self, cx, cy, r, thick, color):
        """A circle outline: outer circle minus inner circle."""
        outer = []
        inner = []
        for i in range(28):
            a = 6.283185307179586 * i / 28.0
            outer.append((cx + (r + thick * 0.5) * _cos(a), cy + (r + thick * 0.5) * _sin(a)))
            inner.append((cx + (r - thick * 0.5) * _cos(a), cy + (r - thick * 0.5) * _sin(a)))
        self._ring(outer, inner, color)

    def _ring(self, outer, inner, color):
        # fill outer, then punch inner back to background is not safe here,
        # so draw as a polygon with a hole using per-row scan of both loops.
        P = [(x * SS, y * SS) for (x, y) in outer]
        Q = [(x * SS, y * SS) for (x, y) in inner]
        ys = [p[1] for p in P]
        y0 = max(0, int(min(ys)))
        y1 = min(self.H - 1, int(max(ys) + 0.999))
        for yy in range(y0, y1 + 1):
            sy = yy + 0.5
            xs = []
            for loop in (P, Q):
                n = len(loop)
                for i in range(n):
                    ax, ay = loop[i]
                    bx, by = loop[(i + 1) % n]
                    if ay == by:
                        continue
                    if (ay <= sy < by) or (by <= sy < ay):
                        t = (sy - ay) / (by - ay)
                        xs.append(ax + t * (bx - ax))
            if len(xs) < 4:
                continue
            xs.sort()
            self._rowspan(yy, int(xs[0] + 0.5), int(xs[1] + 0.5), color)
            self._rowspan(yy, int(xs[2] + 0.5), int(xs[3] + 0.5), color)

    def seg(self, x0, y0, x1, y1, thick, color):
        """Thick straight segment with butt caps."""
        dx = x1 - x0
        dy = y1 - y0
        d = (dx * dx + dy * dy) ** 0.5
        if d < 1e-9:
            self.circle(x0, y0, thick * 0.5, color)
            return
        nx = -dy / d * thick * 0.5
        ny = dx / d * thick * 0.5
        self.poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny),
                   (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], color)

    def path(self, pts, thick, color, closed=False):
        seq = list(pts)
        if closed:
            seq = seq + [seq[0]]
        for i in range(len(seq) - 1):
            self.seg(seq[i][0], seq[i][1], seq[i + 1][0], seq[i + 1][1], thick, color)
        if thick > 2.2:
            for (x, y) in seq[1:-1]:
                self.circle(x, y, thick * 0.5, color)

    def arc(self, cx, cy, r, a0, a1, thick, color, steps=14):
        pts = []
        for i in range(steps + 1):
            a = a0 + (a1 - a0) * i / steps
            pts.append((cx + r * _cos(a), cy + r * _sin(a)))
        self.path(pts, thick, color)

    def wedge(self, cx, cy, r, a0, a1, color, steps=20):
        pts = [(cx, cy)]
        for i in range(steps + 1):
            a = a0 + (a1 - a0) * i / steps
            pts.append((cx + r * _cos(a), cy + r * _sin(a)))
        self.poly(pts, color)

    def wedge_ring(self, cx, cy, r0, r1, a0, a1, color, steps=20):
        outer = []
        inner = []
        for i in range(steps + 1):
            a = a0 + (a1 - a0) * i / steps
            outer.append((cx + r1 * _cos(a), cy + r1 * _sin(a)))
            inner.append((cx + r0 * _cos(a), cy + r0 * _sin(a)))
        self._ring(outer, inner, color)

    # -- text --------------------------------------------------------------
    def text(self, x, y, size, s, color, tracking=0.0, weight=1.0, align="left"):
        """Draw stroke text. y is the cap-height TOP. Returns the advance width."""
        w = text_width(size, s, tracking)
        if align == "right":
            x = x - w
        elif align == "center":
            x = x - w * 0.5
        scale = size / 6.0
        thick = max(1.0, size * 0.145) * weight
        pen = x
        for ch in s:
            g = GLYPHS.get(ch)
            if g is None:
                g = GLYPHS.get("?")
            adv = ADV.get(ch, 5.2)
            for stroke in g:
                pts = [(pen + px * scale, y + py * scale) for (px, py) in stroke]
                if len(pts) == 1:
                    self.circle(pts[0][0], pts[0][1], thick * 0.5, color)
                else:
                    self.path(pts, thick, color)
            pen += (adv * scale) + tracking
        return w

    def roundrect(self, x, y, w, h, r, color):
        self.rect(x + r, y, w - 2 * r, h, color)
        self.rect(x, y + r, r, h - 2 * r, color)
        self.rect(x + w - r, y + r, r, h - 2 * r, color)
        for (cx, cy, a0) in ((x + r, y + r, 3.141592653589793),
                             (x + w - r, y + r, 4.71238898038469),
                             (x + w - r, y + h - r, 0.0),
                             (x + r, y + h - r, 1.5707963267948966)):
            self.wedge(cx, cy, r, a0, a0 + 1.5707963267948966, color, 8)

    def roundrect_ring(self, x, y, w, h, r, thick, color):
        pts = []
        # top edge
        pts += [(x + r, y), (x + w - r, y)]
        pts += [(x + w, y + r), (x + w, y + h - r)]
        pts += [(x + w - r, y + h), (x + r, y + h)]
        pts += [(x, y + h - r), (x, y + r)]
        self.path(pts, thick, color)
        for (cx, cy, a0) in ((x + w - r, y + r, -1.5707963267948966),
                             (x + w - r, y + h - r, 0.0),
                             (x + r, y + h - r, 1.5707963267948966),
                             (x + r, y + r, 3.141592653589793)):
            self.arc(cx, cy, r, a0, a0 + 1.5707963267948966, thick, color, 6)

    # -- output ------------------------------------------------------------
    def resolve(self):
        """Box-filter down to 1x and return (w, h, rgb bytes)."""
        W, H = self.W, self.H
        src = self.buf
        out = bytearray(self.w * self.h * 3)
        s = SS * SS
        o = 0
        for y in range(self.h):
            r0 = (y * SS) * W * 3
            r1 = r0 + W * 3
            for x in range(self.w):
                c0 = r0 + x * SS * 3
                c1 = c0 + 3
                acc0 = src[c0] + src[c1] + src[r1 + x * SS * 3] + src[r1 + x * SS * 3 + 3]
                acc1 = src[c0 + 1] + src[c1 + 1] + src[r1 + x * SS * 3 + 1] + src[r1 + x * SS * 3 + 4]
                acc2 = src[c0 + 2] + src[c1 + 2] + src[r1 + x * SS * 3 + 2] + src[r1 + x * SS * 3 + 5]
                out[o] = acc0 // s
                out[o + 1] = acc1 // s
                out[o + 2] = acc2 // s
                o += 3
        return self.w, self.h, bytes(out)


def _cos(a):
    import math
    return math.cos(a)


def _sin(a):
    import math
    return math.sin(a)


def text_width(size, s, tracking=0.0):
    scale = size / 6.0
    w = 0.0
    for ch in s:
        w += ADV.get(ch, 5.2) * scale + tracking
    return w - tracking if s else 0.0


def wrap(size, s, maxw, tracking=0.0):
    """Greedy word wrap; returns a list of lines."""
    words = s.split()
    lines = []
    cur = ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if text_width(size, trial, tracking) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def png_bytes(w, h, rgb):
    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw.append(0)
        raw += rgb[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


# --------------------------------------------------------------------------
# stroke font: cap height 6 units (0 = cap top, 6 = baseline),
# x-height top 2.5, ascender 0, descender 7.8, advance ~5.2
# --------------------------------------------------------------------------

GLYPHS = {
    "A": [((0, 6), (2, 0), (4, 6)), ((0.85, 3.9), (3.15, 3.9))],
    "B": [((0, 6), (0, 0), (2.6, 0), (3.6, 0.9), (3.6, 2.1), (2.6, 3), (0, 3)),
          ((0, 3), (2.9, 3), (4, 4.1), (4, 4.9), (2.9, 6), (0, 6))],
    "C": [((4, 1.15), (3.2, 0), (1.4, 0), (0, 1.2), (0, 4.8), (1.4, 6), (3.2, 6), (4, 4.85))],
    "D": [((0, 0), (0, 6), (2.3, 6), (4, 4.4), (4, 1.6), (2.3, 0), (0, 0))],
    "E": [((4, 0), (0, 0), (0, 6), (4, 6)), ((0, 3), (3.0, 3))],
    "F": [((4, 0), (0, 0), (0, 6)), ((0, 3), (3.0, 3))],
    "G": [((4, 1.15), (3.2, 0), (1.4, 0), (0, 1.2), (0, 4.8), (1.4, 6), (3.2, 6), (4, 4.85), (4, 3.4), (2.3, 3.4))],
    "H": [((0, 0), (0, 6)), ((4, 0), (4, 6)), ((0, 3), (4, 3))],
    "I": [((1.6, 0), (1.6, 6))],
    "J": [((3.5, 0), (3.5, 4.9), (2.6, 6), (1.2, 6), (0.3, 5.0))],
    "K": [((0, 0), (0, 6)), ((4, 0), (0, 3.5)), ((1.25, 2.6), (4, 6))],
    "L": [((0, 0), (0, 6), (4, 6))],
    "M": [((0, 6), (0, 0), (2, 3.6), (4, 0), (4, 6))],
    "N": [((0, 6), (0, 0), (4, 6), (4, 0))],
    "O": [((1.4, 0), (2.6, 0), (4, 1.2), (4, 4.8), (2.6, 6), (1.4, 6), (0, 4.8), (0, 1.2), (1.4, 0))],
    "P": [((0, 6), (0, 0), (2.7, 0), (4, 1.2), (4, 2.3), (2.7, 3.4), (0, 3.4))],
    "Q": [((1.4, 0), (2.6, 0), (4, 1.2), (4, 4.8), (2.6, 6), (1.4, 6), (0, 4.8), (0, 1.2), (1.4, 0)),
          ((2.5, 4.2), (4.2, 6.4))],
    "R": [((0, 6), (0, 0), (2.7, 0), (4, 1.2), (4, 2.3), (2.7, 3.4), (0, 3.4)),
          ((2.1, 3.4), (4, 6))],
    "S": [((4, 1.15), (3.2, 0), (1.3, 0), (0, 1.1), (0, 1.9), (1.3, 3), (2.6, 3),
           (4, 4.1), (4, 4.9), (2.6, 6), (1.1, 6), (0, 4.9))],
    "T": [((0, 0), (4, 0)), ((2, 0), (2, 6))],
    "U": [((0, 0), (0, 4.8), (1.4, 6), (2.6, 6), (4, 4.8), (4, 0))],
    "V": [((0, 0), (2, 6), (4, 0))],
    "W": [((0, 0), (1, 6), (2, 2.3), (3, 6), (4, 0))],
    "X": [((0, 0), (4, 6)), ((4, 0), (0, 6))],
    "Y": [((0, 0), (2, 3), (4, 0)), ((2, 3), (2, 6))],
    "Z": [((0, 0), (4, 0), (0, 6), (4, 6))],

    "a": [((1.0, 2.5), (2.7, 2.5), (3.5, 3.3), (3.5, 5.2), (2.7, 6), (1.0, 6),
           (0.2, 5.2), (0.2, 3.3), (1.0, 2.5)), ((3.5, 2.5), (3.5, 6))],
    "b": [((0, 0), (0, 6)), ((0, 3.3), (0.8, 2.5), (2.5, 2.5), (3.4, 3.3),
                             (3.4, 5.2), (2.5, 6), (0.8, 6), (0, 5.2))],
    "c": [((3.3, 3.05), (2.5, 2.5), (1.0, 2.5), (0.2, 3.3), (0.2, 5.2), (1.0, 6),
           (2.5, 6), (3.3, 5.45))],
    "d": [((3.4, 0), (3.4, 6)), ((3.4, 3.3), (2.6, 2.5), (0.9, 2.5), (0, 3.3),
                                 (0, 5.2), (0.9, 6), (2.6, 6), (3.4, 5.2))],
    "e": [((0.2, 4.15), (3.4, 4.15), (3.4, 3.2), (2.6, 2.5), (1.0, 2.5), (0.2, 3.3),
           (0.2, 5.2), (1.0, 6), (2.5, 6), (3.3, 5.45))],
    "f": [((3.2, 0.3), (2.4, 0), (1.8, 0), (1.2, 0.6), (1.2, 6)), ((0.2, 2.5), (2.8, 2.5))],
    "g": [((3.4, 2.5), (3.4, 6.8), (2.5, 7.6), (1.0, 7.6), (0.3, 7.05)),
          ((3.4, 3.3), (2.6, 2.5), (0.9, 2.5), (0, 3.3), (0, 5.2), (0.9, 6),
           (2.6, 6), (3.4, 5.2))],
    "h": [((0, 0), (0, 6)), ((0, 3.3), (0.8, 2.5), (2.6, 2.5), (3.4, 3.3), (3.4, 6))],
    "i": [((1.6, 0.35), (1.6, 0.55)), ((1.6, 2.5), (1.6, 6))],
    "j": [((2.4, 0.35), (2.4, 0.55)), ((2.4, 2.5), (2.4, 7.0), (1.7, 7.6), (0.7, 7.6), (0.2, 7.1))],
    "k": [((0, 0), (0, 6)), ((3.2, 2.5), (0, 4.9)), ((1.15, 4.0), (3.3, 6))],
    "l": [((1.4, 0), (1.4, 6))],
    "m": [((0, 2.5), (0, 6)), ((0, 3.4), (0.7, 2.5), (1.5, 3.4), (1.5, 6)),
          ((1.5, 3.4), (2.2, 2.5), (3.0, 3.4), (3.0, 6))],
    "n": [((0, 2.5), (0, 6)), ((0, 3.3), (0.9, 2.5), (2.5, 2.5), (3.4, 3.3), (3.4, 6))],
    "o": [((1.0, 2.5), (2.6, 2.5), (3.4, 3.3), (3.4, 5.2), (2.6, 6), (1.0, 6),
           (0.2, 5.2), (0.2, 3.3), (1.0, 2.5))],
    "p": [((0, 2.5), (0, 7.8)), ((0, 3.3), (0.8, 2.5), (2.5, 2.5), (3.4, 3.3),
                                 (3.4, 5.2), (2.5, 6), (0.8, 6), (0, 5.2))],
    "q": [((3.4, 2.5), (3.4, 7.8)), ((3.4, 3.3), (2.6, 2.5), (0.9, 2.5), (0, 3.3),
                                    (0, 5.2), (0.9, 6), (2.6, 6), (3.4, 5.2))],
    "r": [((0, 2.5), (0, 6)), ((0, 3.4), (0.9, 2.5), (2.4, 2.5), (3.2, 3.1))],
    "s": [((3.2, 3.0), (2.5, 2.5), (1.0, 2.5), (0.3, 3.0), (0.3, 3.7), (1.0, 4.2),
           (2.5, 4.3), (3.2, 4.9), (3.2, 5.5), (2.5, 6), (1.0, 6), (0.3, 5.5))],
    "t": [((1.4, 0.8), (1.4, 5.4), (1.95, 6), (2.9, 6)), ((0.2, 2.5), (2.8, 2.5))],
    "u": [((0, 2.5), (0, 5.2), (0.9, 6), (2.4, 6), (3.4, 5.2)), ((3.4, 2.5), (3.4, 6))],
    "v": [((0, 2.5), (1.7, 6), (3.4, 2.5))],
    "w": [((0, 2.5), (0.9, 6), (1.7, 3.9), (2.5, 6), (3.4, 2.5))],
    "x": [((0, 2.5), (3.4, 6)), ((3.4, 2.5), (0, 6))],
    "y": [((0, 2.5), (1.7, 6.1)), ((3.4, 2.5), (1.15, 7.9), (0.45, 7.9))],
    "z": [((0, 2.5), (3.4, 2.5), (0, 6), (3.4, 6))],

    "0": [((1.4, 0), (2.6, 0), (4, 1.2), (4, 4.8), (2.6, 6), (1.4, 6), (0, 4.8), (0, 1.2), (1.4, 0))],
    "1": [((0.7, 1.3), (2.0, 0), (2.0, 6)), ((0.7, 6), (3.3, 6))],
    "2": [((0, 1.15), (1.4, 0), (2.8, 0), (4, 1.2), (4, 2.1), (0, 6), (4, 6))],
    "3": [((0, 0.4), (3.0, 0), (1.9, 2.6), (2.9, 2.6), (4, 3.7), (4, 4.9),
           (2.7, 6), (1.1, 6), (0, 5.1))],
    "4": [((3.0, 6), (3.0, 0), (0, 4.2), (4, 4.2))],
    "5": [((4, 0), (0.35, 0), (0.35, 2.5), (2.7, 2.5), (4, 3.8), (4, 4.9),
           (2.6, 6), (1.0, 6), (0, 5.0))],
    "6": [((3.8, 0.55), (2.6, 0), (1.6, 0), (0, 1.6), (0, 4.8), (1.2, 6),
           (2.8, 6), (4, 4.8), (4, 3.9), (2.8, 2.7), (0, 3.3))],
    "7": [((0, 0), (4, 0), (1.6, 6))],
    "8": [((1.2, 3), (0.3, 2.2), (0.3, 1.0), (1.4, 0), (2.6, 0), (3.7, 1.0),
           (3.7, 2.2), (2.8, 3), (1.2, 3), (0.15, 4.0), (0.15, 5.1),
           (1.3, 6), (2.7, 6), (3.85, 5.1), (3.85, 4.0), (2.8, 3))],
    "9": [((0.2, 5.45), (1.4, 6), (2.4, 6), (4, 4.4), (4, 1.2), (2.8, 0),
           (1.2, 0), (0, 1.2), (0, 2.1), (1.2, 3.3), (4, 2.7))],

    " ": [],
    ".": [((1.6, 5.7), (1.6, 6))],
    ",": [((1.75, 5.6), (1.4, 6.9))],
    ":": [((1.6, 3.0), (1.6, 3.5)), ((1.6, 5.7), (1.6, 6.2))],
    ";": [((1.6, 3.0), (1.6, 3.5)), ((1.75, 5.6), (1.4, 6.9))],
    "-": [((0.6, 4.2), (3.2, 4.2))],
    "\u2013": [((0.4, 4.2), (3.4, 4.2))],
    "\u2014": [((0, 4.2), (4, 4.2))],
    "\u00b7": [((1.8, 4.05), (1.8, 4.35))],
    "/": [((0, 6.4), (3.6, -0.4))],
    "(": [((2.9, -0.5), (1.7, 1.2), (1.7, 4.8), (2.9, 6.5))],
    ")": [((0.9, -0.5), (2.1, 1.2), (2.1, 4.8), (0.9, 6.5))],
    "'": [((1.6, 0), (1.6, 1.7))],
    "\u2019": [((1.7, 0), (1.4, 1.7))],
    "\u2018": [((1.5, 0), (1.8, 1.7))],
    '"': [((1.0, 0), (1.0, 1.7)), ((2.5, 0), (2.5, 1.7))],
    "!": [((1.6, 0), (1.6, 4.1)), ((1.6, 5.7), (1.6, 6))],
    "?": [((0.25, 1.2), (1.0, 0.1), (2.6, 0.1), (3.45, 1.2), (3.45, 2.0),
           (1.95, 3.05), (1.95, 4.0)), ((1.95, 5.7), (1.95, 6))],
    "+": [((1.9, 2.0), (1.9, 5.0)), ((0.4, 3.5), (3.4, 3.5))],
    "=": [((0.5, 2.7), (3.4, 2.7)), ((0.5, 4.3), (3.4, 4.3))],
    "%": [((0, 0.3), (3.6, 5.7)), ((0.9, 0.9), (0.9, 1.3)), ((2.7, 4.7), (2.7, 5.1))],
    "\u00b0": [((1.1, 1.5), (1.9, 0.7), (2.7, 1.5), (1.9, 2.3), (1.1, 1.5))],
    "\u2192": [((0, 4.0), (3.6, 4.0)), ((2.4, 2.7), (3.9, 4.0), (2.4, 5.3))],
    "\u2022": [((1.5, 4.0), (1.9, 4.0))],
    "$": [((3.5, 1.0), (2.7, 0.15), (1.2, 0.15), (0.25, 1.0), (0.25, 1.8),
           (1.3, 2.8), (2.5, 2.9), (3.5, 3.9), (3.5, 4.8), (2.5, 5.85),
           (1.0, 5.85), (0.15, 5.0)), ((1.85, -0.5), (1.85, 6.5))],
    "&": [((4.0, 6.0), (1.3, 2.2), (1.3, 1.0), (2.2, 0), (3.1, 1.0), (1.2, 3.2),
           (0.2, 4.4), (0.9, 6.0), (2.2, 6.0), (4.0, 3.6))],
    "#": [((1.2, 0), (0.8, 6)), ((3.0, 0), (2.6, 6)), ((0.2, 2.1), (3.8, 2.1)), ((0.1, 4.0), (3.7, 4.0))],
}

ADV = {
    " ": 2.6, ".": 2.6, ",": 2.6, ":": 2.6, ";": 2.6, "'": 2.2, "\u2019": 2.2,
    "\u2018": 2.2, '"': 3.2, "!": 2.8, "?": 4.2, "-": 3.6, "\u2013": 3.8,
    "\u2014": 4.4, "\u00b7": 2.6, "\u2022": 3.2, "/": 3.6, "(": 2.9, ")": 2.9,
    "I": 3.2, "J": 4.5, "L": 4.6, "T": 4.7, "1": 4.4, "l": 2.8, "i": 2.8,
    "j": 3.2, "t": 3.4, "f": 3.4, "r": 3.4, "s": 4.0, "c": 4.2, "k": 4.2,
    "y": 4.4, "v": 4.4, "w": 4.6, "x": 4.4, "z": 4.2, "\u00b0": 3.2,
    "\u2192": 4.6, "a": 4.4, "b": 4.4, "d": 4.4, "e": 4.4, "g": 4.4, "h": 4.4,
    "n": 4.4, "o": 4.4, "p": 4.4, "q": 4.4, "u": 4.4, "$": 4.4, "&": 4.4,
    "#": 4.2, "+": 4.0, "=": 4.0, "%": 4.2,
}

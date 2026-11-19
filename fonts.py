"""Fonts: variable-weight faces from Google Fonts, loaded from ./fonts.

The program renders at 2x and downsamples, so text stays crisp when the PNG is
read at 300px wide. Only PIL is used; the final image ships in the repo, so the
build needs no network and no font files at run time.
"""
import os
from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FDIR = os.path.join(HERE, "fonts")

_cache = {}


def face(name, size, weight=None, width=None):
    """A face at `size` px, at an optional weight (100-900) and width (62-125)."""
    key = (name, size, weight, width)
    if key in _cache:
        return _cache[key]
    path = os.path.join(FDIR, name + ".ttf")
    if not os.path.exists(path):
        path = name  # allow an absolute path
    f = ImageFont.truetype(path, size)
    axes = {}
    for a in f.get_variation_axes():
        n = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
        axes[n.lower()] = a
    if weight is not None and "weight" in axes:
        f.set_variation_by_axes(_axes(f, weight, width))
    _cache[key] = f
    return f


def _axes(f, weight, width):
    vals = []
    for a in f.get_variation_axes():
        n = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
        n = n.lower()
        if n == "weight":
            vals.append(weight)
        elif n in ("width", "optical size", "optical size"):
            vals.append(width if (width is not None and n == "width") else a["default"])
        else:
            vals.append(a["default"])
    return vals


# Short names used by the layouts.
def serif(size, w=700):
    return face("pfd", size, w)


def text(size, w=400):
    return face("sserif", size, w)


def sans(size, w=500, wd=None):
    return face("archivo", size, w, wd)


def cond(size, w=600):
    return face("oswald", size, w)


def caps(size, w=600):
    return face("inter", size, w)

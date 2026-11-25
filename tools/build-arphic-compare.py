#!/usr/bin/env python3
"""Generate assets/arphic-compare-data.js for arphic-compare.html.

For every codepoint covered by any of the six Arphic Kai faces, records which
of the faces have it and which of them share a byte-identical outline. The page
uses that to (a) blank out cells the face does not cover, so system fallback
cannot masquerade as a real glyph, and (b) label the cells so identical shapes
are visible at a glance.

It also scores how differently two faces actually *draw* a shared codepoint, by
rasterising both and comparing pixels. Outline point counts are useless for this
— the faces were digitised separately, so point counts differ everywhere even
when the shapes are indistinguishable. Each glyph is normalised to its ink
bounding box first, so a glyph that is merely drawn slightly larger or shifted
does not read as a different shape; what survives is genuine structural
difference (the 匕 component, the 真/直 interior, 亡 …).

Reads the upstream sources each package's build.py downloads into src/, so run
the three build.py scripts first (or at least their download step).

Usage:
    pip install fonttools brotli pillow numpy
    python3 tools/build-arphic-compare.py      # a few minutes; rasterises ~14k pairs
"""

import hashlib
import json
import os
import sys

import numpy as np
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTCollection, TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "arphic-compare-data.js")

# Display order == column order on the page.
FACES = [
    {"key": "gb", "family": "AR PL KaitiM GB", "zh": "簡中楷 GB", "en": "KaitiM GB",
     "css": "./arphic-kaitim-gb/arphic-kaitim-gb.css",
     "src": ("arphic-kaitim-gb/src/gkai00mp.ttf", None)},
    {"key": "big5", "family": "AR PL KaitiM Big5", "zh": "中楷 Big5", "en": "KaitiM Big5",
     "css": "./arphic-kaitim-big5/arphic-kaitim-big5.css",
     "src": ("arphic-kaitim-big5/src/bkai00mp.ttf", None)},
    {"key": "ukai-cn", "family": "AR PL UKai CN", "zh": "UKai CN", "en": "UKai CN",
     "css": "./arphic-ukai/arphic-ukai.css", "src": ("arphic-ukai/src/ukai.ttc", 0)},
    {"key": "ukai-hk", "family": "AR PL UKai HK", "zh": "UKai HK", "en": "UKai HK",
     "css": "./arphic-ukai/arphic-ukai.css", "src": ("arphic-ukai/src/ukai.ttc", 1)},
    {"key": "ukai-tw", "family": "AR PL UKai TW", "zh": "UKai TW", "en": "UKai TW",
     "css": "./arphic-ukai/arphic-ukai.css", "src": ("arphic-ukai/src/ukai.ttc", 2)},
    {"key": "ukai-tw-mbe", "family": "AR PL UKai TW MBE", "zh": "UKai TW MBE", "en": "UKai TW MBE",
     "css": "./arphic-ukai/arphic-ukai.css", "src": ("arphic-ukai/src/ukai.ttc", 3)},
]

LETTERS = "abcdef"  # one per face, in FACES order


def open_face(path, index):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        sys.exit(f"missing {path} — run the package's build.py to fetch it first")
    if index is None:
        return TTFont(full)
    return TTCollection(full).fonts[index]


def outlines(font):
    """-> (cp -> outline signature, cp -> (point count, contour count))"""
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    hmtx = font["hmtx"]
    sigs, shape = {}, {}
    for cp, name in cmap.items():
        pen = DecomposingRecordingPen(glyphs)
        try:
            glyphs[name].draw(pen)
        except Exception:
            continue
        h = hashlib.md5(repr(pen.value).encode()).hexdigest()
        sigs[cp] = f"{h}:{hmtx[name][0]}"
        npts = sum(len(seg[1] or ()) for seg in pen.value)
        shape[cp] = (npts, sum(1 for seg in pen.value if seg[0] == "moveTo"))
    return sigs, shape


# ── pixel comparison ──────────────────────────────────────────────────────────
RASTER = 96      # px the glyph is drawn at
BOX = 96         # px the ink box is normalised to
SHIFT = 2        # residual alignment search, in px


def raster_font(path, index):
    return ImageFont.truetype(os.path.join(ROOT, path), RASTER,
                              **({} if index is None else {"index": index}))


def ink_mask(font, ch):
    """Glyph rasterised, cropped to its ink box and scaled to BOX×BOX."""
    pad = RASTER // 2
    im = Image.new("L", (RASTER + 2 * pad, RASTER + 2 * pad), 0)
    ImageDraw.Draw(im).text((pad, pad + RASTER), ch, font=font, fill=255, anchor="ls")
    im = im.point(lambda v: 255 if v >= 110 else 0)
    box = im.getbbox()
    if not box:
        return None
    im = im.crop(box).resize((BOX, BOX), Image.LANCZOS).point(lambda v: 255 if v >= 110 else 0)
    return np.array(im) > 0


def _dilate(mask):
    return np.array(Image.fromarray((mask * 255).astype("uint8"))
                    .filter(ImageFilter.MaxFilter(5))) > 0


def shape_distance(a, b):
    """0 = indistinguishable, ~0.3 = clearly a different shape.

    Pixels of one glyph that fall outside a slightly grown version of the other,
    minimised over a small shift so sub-pixel fitting differences do not count.
    """
    if a is None or b is None:
        return 0.0
    if not a.any() or not b.any():
        return 0.0
    grown_a, grown_b, total = _dilate(a), _dilate(b), a.sum() + b.sum()
    best = 1.0
    for dy in range(-SHIFT, SHIFT + 1):
        for dx in range(-SHIFT, SHIFT + 1):
            shifted = np.roll(np.roll(b, dy, 0), dx, 1)
            grown = np.roll(np.roll(grown_b, dy, 0), dx, 1)
            d = ((a & ~grown).sum() + (shifted & ~grown_a).sum()) / total
            best = min(best, d)
            if best == 0.0:
                return 0.0
    return best


def gb2312_hanzi():
    s = set()
    for hi in range(0xA1, 0xFF):
        for lo in range(0xA1, 0xFF):
            try:
                ch = bytes([hi, lo]).decode("gb2312")
            except Exception:
                continue
            s.add(ord(ch))
    return s


def big5_hanzi():
    s = set()
    for hi in range(0xA1, 0xFA):
        for lo in list(range(0x40, 0x7F)) + list(range(0xA1, 0xFF)):
            try:
                ch = bytes([hi, lo]).decode("big5")
            except Exception:
                continue
            s.add(ord(ch))
    return s


def main():
    sigs, shapes = {}, {}
    for face in FACES:
        font = open_face(*face["src"])
        sigs[face["key"]], shapes[face["key"]] = outlines(font)
        print(f"{face['family']}: {len(sigs[face['key']])} codepoints")

    every = sorted(set().union(*(set(s) for s in sigs.values())))
    gb2312, big5 = gb2312_hanzi(), big5_hanzi()

    # Per codepoint: one letter per face, '-' when the face lacks it, otherwise
    # the letter of the first face carrying the identical outline. So 'ab bbb-'
    # reads "face 1 stands alone, faces 2-5 share one shape, face 6 lacks it".
    # Pixel comparison, only where it answers something: how far apart the two
    # classic faces draw a shared codepoint, and — where they disagree — which
    # of them UKai CN actually looks like.
    by_key = {f["key"]: f for f in FACES}
    raster = {k: raster_font(*by_key[k]["src"]) for k in ("gb", "big5", "ukai-cn")}

    vis, vis_cn_gb, vis_cn_b5 = {}, {}, {}
    todo = [cp for cp in every
            if cp in sigs["gb"] and cp in sigs["big5"] and sigs["gb"][cp] != sigs["big5"][cp]]
    print(f"rasterising {len(todo)} disputed codepoints …")
    for n, cp in enumerate(todo, 1):
        ch = chr(cp)
        mg, mb = ink_mask(raster["gb"], ch), ink_mask(raster["big5"], ch)
        vis[cp] = shape_distance(mg, mb)
        if cp in sigs["ukai-cn"]:
            mc = ink_mask(raster["ukai-cn"], ch)
            vis_cn_gb[cp] = shape_distance(mc, mg)
            vis_cn_b5[cp] = shape_distance(mc, mb)
        if n % 500 == 0:
            print(f"  {n}/{len(todo)}")

    def enc(d):
        """distance -> one char, chr(33) = identical, capped at 30% apart."""
        return chr(33 + min(89, round(d * 300)))

    patterns, pattern_ids, flags = [], [], []
    index = {}
    for cp in every:
        seen, row = {}, []
        for i, face in enumerate(FACES):
            sig = sigs[face["key"]].get(cp)
            if sig is None:
                row.append("-")
                continue
            row.append(seen.setdefault(sig, LETTERS[i]))
        pat = "".join(row)
        if pat not in index:
            index[pat] = len(patterns)
            patterns.append(pat)
        pattern_ids.append(index[pat])
        flags.append((1 if cp in gb2312 else 0) | (2 if cp in big5 else 0))

    if len(patterns) > 90:  # encoded one char per codepoint from '!' upwards
        sys.exit(f"too many distinct patterns ({len(patterns)}) for the encoding")

    payload = {
        "note": "Generated by tools/build-arphic-compare.py; do not edit manually.",
        "faces": [{k: f[k] for k in ("key", "family", "zh", "en", "css")} for f in FACES],
        "letters": LETTERS,
        # Codepoints as a plain string; iterate with [...str] to get code points.
        "cps": "".join(chr(cp) for cp in every),
        "patterns": patterns,
        # One char per codepoint: chr(33 + index into patterns).
        "pat": "".join(chr(33 + i) for i in pattern_ids),
        # One char per codepoint: '0'..'3' bitfield, 1 = in GB2312, 2 = in Big5.
        "flags": "".join(str(f) for f in flags),
        # One char per codepoint, chr(33) = same shape / not comparable, each
        # further step = 1/3 of a percent of mismatched ink after normalising
        # size and position. "diff" is GB vs Big5; "cnGb"/"cnBig5" are UKai CN
        # against each classic face, filled in only where the classics disagree.
        "diff": "".join(enc(vis.get(cp, 0.0)) for cp in every),
        "cnGb": "".join(enc(vis_cn_gb[cp]) if cp in vis_cn_gb else " " for cp in every),
        "cnBig5": "".join(enc(vis_cn_b5[cp]) if cp in vis_cn_b5 else " " for cp in every),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("/* Generated by tools/build-arphic-compare.py; do not edit manually. */\n")
        f.write("window.ARPHIC_COMPARE = ")
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print(f"\n{len(every)} codepoints, {len(patterns)} distinct patterns")
    print(f"wrote {OUT} ({os.path.getsize(OUT) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()

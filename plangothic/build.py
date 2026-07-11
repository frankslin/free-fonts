#!/usr/bin/env python3
"""Build chunked woff2 + CSS for the Plangothic / 遍黑體 webfont package.

Downloads PlangothicP1-Regular.ttf and PlangothicP2-Regular.ttf from the
upstream GitHub release, slices each into 256-codepoint woff2 chunks, and
generates plangothic.css with all rules sharing font-family 'Plangothic'.

P1 and P2 have disjoint codepoints, so browsers select the correct file via
unicode-range without any JS coordination.

Usage:
    pip install fonttools brotli
    python3 build.py            # download to src/ + build all chunks
    python3 build.py --no-dl    # skip download (src/*.ttf already present)
    python3 build.py --jobs N   # explicit parallelism
"""

import argparse
import logging
import urllib.request
from multiprocessing import Pool, cpu_count
from pathlib import Path

from fontTools import subset as ft_subset
from fontTools.ttLib import TTFont

logging.getLogger("fontTools").setLevel(logging.ERROR)

ROOT = Path(__file__).parent
SRC_DIR = ROOT / "src"
FONTS_DIR = ROOT / "fonts"
CSS_PATH = ROOT / "plangothic.css"
CHUNK_SIZE = 0x100

RELEASE_BASE = (
    "https://github.com/Fitzgerald-Porthmouth-Koenigsegg/Plangothic_Project"
    "/releases/download/V2.9.5795"
)

SOURCES = [
    {
        "file": "PlangothicP1-Regular.ttf",
        "prefix": "PlangothicP1",
        "note": "P1: BMP URO + Ext-A/B/C/D/E/F/G/H (CJK main planes)",
    },
    {
        "file": "PlangothicP2-Regular.ttf",
        "prefix": "PlangothicP2",
        "note": "P2: Ext-B/C/D/E/F/G/H overflow + compatibility & symbols",
    },
]

FAMILY = "Plangothic"
WEIGHT = 400


def download() -> None:
    SRC_DIR.mkdir(exist_ok=True)
    for src in SOURCES:
        dest = SRC_DIR / src["file"]
        if dest.exists():
            print(f"{dest.name} already present, skipping download.")
            continue
        url = f"{RELEASE_BASE}/{src['file']}"
        print(f"Downloading {url} ...")
        urllib.request.urlretrieve(url, dest)
        print(f"  {dest.stat().st_size / 1024 / 1024:.1f} MB -> {dest}")


def _build_chunk(args: tuple) -> tuple[str, int]:
    ttf_path, cps, out_path = args
    options = ft_subset.Options()
    options.flavor = "woff2"
    options.name_IDs = [1, 2, 4]
    options.layout_features = []
    options.drop_tables += ["DSIG", "morx", "prop", "GDEF", "GPOS", "GSUB"]

    font = ft_subset.load_font(ttf_path, options)
    subsetter = ft_subset.Subsetter(options=options)
    subsetter.populate(unicodes=sorted(cps))
    subsetter.subset(font)
    ft_subset.save_font(font, out_path, options)
    font.close()
    p = Path(out_path)
    return p.name, p.stat().st_size


def unicode_range_str(start: int) -> str:
    end = start + CHUNK_SIZE - 1
    if end <= 0xFFFF:
        return f"U+{start:04X}-{end:04X}"
    return f"U+{start:05X}-{end:05X}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-dl", action="store_true", help="Skip download step")
    ap.add_argument("--jobs", type=int, default=cpu_count(), metavar="N")
    args = ap.parse_args()

    if not args.no_dl:
        download()

    FONTS_DIR.mkdir(exist_ok=True)
    sections = []

    for src in SOURCES:
        ttf = SRC_DIR / src["file"]
        prefix = src["prefix"]
        tt = TTFont(str(ttf), lazy=True)
        cps = set(tt.getBestCmap())
        version = tt["name"].getDebugName(5)
        tt.close()

        chunk_map: dict[int, set[int]] = {}
        for cp in cps:
            chunk_map.setdefault((cp // CHUNK_SIZE) * CHUNK_SIZE, set()).add(cp)
        print(f"{ttf.name}: {len(cps):,} cps, {len(chunk_map)} chunks, {version}")

        tasks = [
            (str(ttf), chunk_cps,
             str(FONTS_DIR / f"{prefix}-{WEIGHT}-{start:06x}.woff2"))
            for start, chunk_cps in sorted(chunk_map.items())
        ]
        with Pool(processes=args.jobs) as pool:
            for i, (name, size) in enumerate(pool.imap_unordered(_build_chunk, tasks), 1):
                if i % 50 == 0 or i == len(tasks):
                    print(f"  [{i}/{len(tasks)}] {name} {size // 1024} KB")

        rules = []
        for start in sorted(chunk_map):
            rules.append(
                "@font-face {\n"
                f"  font-family: '{FAMILY}';\n"
                "  font-style: normal;\n"
                f"  font-weight: {WEIGHT};\n"
                "  font-display: swap;\n"
                f"  src: url('fonts/{prefix}-{WEIGHT}-{start:06x}.woff2') format('woff2');\n"
                f"  unicode-range: {unicode_range_str(start)};\n"
                "}"
            )
        sections.append(f"/* {src['note']} */\n\n" + "\n\n".join(rules))

    header = (
        "/* Plangothic / 遍黑體 Webfonts\n"
        " * Upstream: https://github.com/Fitzgerald-Porthmouth-Koenigsegg/Plangothic_Project"
        " release V2.9.5795\n"
        " * Generated CSS; do not edit manually.\n"
        " * Chunk size: 256 codepoints.\n"
        " */\n\n"
    )
    CSS_PATH.write_text(header + "\n\n".join(sections) + "\n", encoding="utf-8")
    total = sum(s.count("@font-face") for s in sections)
    print(f"\nCSS -> {CSS_PATH} ({total} @font-face rules)")


if __name__ == "__main__":
    main()

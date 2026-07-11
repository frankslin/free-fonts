#!/usr/bin/env python3
"""Build chunked woff2 + CSS for the LXGW Marker Gothic webfont package.

Downloads LxgwMarkerGothic-v1.003.zip from the upstream GitHub release,
extracts LXGWMarkerGothic-Regular.ttf, slices it into 256-codepoint woff2
chunks, and generates lxgw-marker-gothic.css.

Usage:
    pip install fonttools brotli
    python3 build.py            # download + extract to src/ + build
    python3 build.py --no-dl    # skip download (src/*.ttf already present)
    python3 build.py --jobs N   # explicit parallelism
"""

import argparse
import logging
import urllib.request
import zipfile
from multiprocessing import Pool, cpu_count
from pathlib import Path

from fontTools import subset as ft_subset
from fontTools.ttLib import TTFont

logging.getLogger("fontTools").setLevel(logging.ERROR)

ROOT = Path(__file__).parent
SRC_DIR = ROOT / "src"
FONTS_DIR = ROOT / "fonts"
CSS_PATH = ROOT / "lxgw-marker-gothic.css"
CHUNK_SIZE = 0x100

RELEASE_URL = (
    "https://github.com/lxgw/LxgwMarkerGothic/releases/download"
    "/v1.003/LxgwMarkerGothic-v1.003.zip"
)
ZIP_NAME = "LxgwMarkerGothic-v1.003.zip"
TTF_NAME = "LXGWMarkerGothic-Regular.ttf"

FAMILY = "LXGW Marker Gothic"
PREFIX = "LXGWMarkerGothic"
WEIGHT = 400


def download() -> None:
    SRC_DIR.mkdir(exist_ok=True)
    dest_ttf = SRC_DIR / TTF_NAME
    if dest_ttf.exists():
        print(f"{TTF_NAME} already present, skipping download.")
        return
    zip_path = SRC_DIR / ZIP_NAME
    if not zip_path.exists():
        print(f"Downloading {RELEASE_URL} ...")
        urllib.request.urlretrieve(RELEASE_URL, zip_path)
        print(f"  {zip_path.stat().st_size / 1024 / 1024:.1f} MB -> {zip_path}")
    print(f"Extracting {TTF_NAME} ...")
    with zipfile.ZipFile(zip_path) as zf:
        candidates = [n for n in zf.namelist() if n.endswith(TTF_NAME)]
        if not candidates:
            raise FileNotFoundError(f"{TTF_NAME} not found in zip; contents: {zf.namelist()}")
        zf.extract(candidates[0], SRC_DIR)
        extracted = SRC_DIR / candidates[0]
        if extracted != dest_ttf:
            extracted.rename(dest_ttf)
    print(f"  -> {dest_ttf}")


def _build_chunk(args: tuple) -> tuple[str, int]:
    ttf_path, cps, out_path = args
    options = ft_subset.Options()
    options.flavor = "woff2"
    options.name_IDs = [1, 2, 4]
    options.drop_tables += ["DSIG"]

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
    ttf = SRC_DIR / TTF_NAME
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
         str(FONTS_DIR / f"{PREFIX}-{WEIGHT}-{start:06x}.woff2"))
        for start, chunk_cps in sorted(chunk_map.items())
    ]
    with Pool(processes=args.jobs) as pool:
        for i, (name, size) in enumerate(pool.imap_unordered(_build_chunk, tasks), 1):
            if i % 40 == 0 or i == len(tasks):
                print(f"  [{i}/{len(tasks)}] {name} {size // 1024} KB")

    rules = []
    for start in sorted(chunk_map):
        rules.append(
            "@font-face {\n"
            f"  font-family: '{FAMILY}';\n"
            "  font-style: normal;\n"
            f"  font-weight: {WEIGHT};\n"
            "  font-display: swap;\n"
            f"  src: url('fonts/{PREFIX}-{WEIGHT}-{start:06x}.woff2') format('woff2');\n"
            f"  unicode-range: {unicode_range_str(start)};\n"
            "}"
        )

    header = (
        "/* LXGW Marker Gothic Webfonts\n"
        " * Upstream: https://github.com/lxgw/LxgwMarkerGothic release v1.003\n"
        " * Generated CSS; do not edit manually.\n"
        " * Chunk size: 256 codepoints.\n"
        " */\n\n"
    )
    CSS_PATH.write_text(header + "\n\n".join(rules) + "\n", encoding="utf-8")
    print(f"\nCSS -> {CSS_PATH} ({len(rules)} @font-face rules)")


if __name__ == "__main__":
    main()

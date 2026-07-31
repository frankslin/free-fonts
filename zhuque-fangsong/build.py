#!/usr/bin/env python3
"""Build chunked woff2 + CSS for the Zhuque Fangsong / 朱雀仿宋 webfont package.

Downloads the ZhuqueFangsong release zip from the upstream GitHub release,
extracts ZhuqueFangsong-Regular.ttf, slices it into 256-codepoint woff2
chunks, and generates zhuque-fangsong.css.

Note: upstream v0.212 is a prerelease ("technical preview") — glyph coverage
and shapes may change between versions.

Usage:
    pip install fonttools brotli
    python3 build.py            # download to src/ + build all chunks
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
CSS_PATH = ROOT / "zhuque-fangsong.css"
CHUNK_SIZE = 0x100

RELEASE_TAG = "v0.212"
ZIP_URL = (
    "https://github.com/TrionesType/zhuque/releases/download/"
    f"{RELEASE_TAG}/ZhuqueFangsong-{RELEASE_TAG}.zip"
)

SOURCES = [
    {"file": "ZhuqueFangsong-Regular.ttf", "weight": 400},
]

FAMILY = "Zhuque Fangsong"
PREFIX = "ZhuqueFangsong"


def download() -> None:
    SRC_DIR.mkdir(exist_ok=True)
    if all((SRC_DIR / src["file"]).exists() for src in SOURCES):
        print("All TTFs already present, skipping download.")
        return
    zip_path = SRC_DIR / ZIP_URL.rsplit("/", 1)[-1]
    print(f"Downloading {ZIP_URL} ...")
    urllib.request.urlretrieve(ZIP_URL, zip_path)
    print(f"  {zip_path.stat().st_size / 1024 / 1024:.1f} MB -> {zip_path}")
    with zipfile.ZipFile(zip_path) as zf:
        for src in SOURCES:
            zf.extract(src["file"], SRC_DIR)
            print(f"  extracted {src['file']}")
    zip_path.unlink()


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
    all_rules: list[tuple[int, int, str]] = []  # (weight, start, rule_text)

    for src in SOURCES:
        ttf = SRC_DIR / src["file"]
        weight = src["weight"]
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
             str(FONTS_DIR / f"{PREFIX}-{weight}-{start:06x}.woff2"))
            for start, chunk_cps in sorted(chunk_map.items())
        ]
        with Pool(processes=args.jobs) as pool:
            for i, (name, size) in enumerate(pool.imap_unordered(_build_chunk, tasks), 1):
                if i % 40 == 0 or i == len(tasks):
                    print(f"  [{i}/{len(tasks)}] {name} {size // 1024} KB")

        for start in sorted(chunk_map):
            rule = (
                "@font-face {\n"
                f"  font-family: '{FAMILY}';\n"
                "  font-style: normal;\n"
                f"  font-weight: {weight};\n"
                "  font-display: swap;\n"
                f"  src: url('fonts/{PREFIX}-{weight}-{start:06x}.woff2') format('woff2');\n"
                f"  unicode-range: {unicode_range_str(start)};\n"
                "}"
            )
            all_rules.append((weight, start, rule))

    all_rules.sort(key=lambda x: (x[0], x[1]))
    header = (
        "/* Zhuque Fangsong / 朱雀仿宋 Webfonts\n"
        f" * Upstream: https://github.com/TrionesType/zhuque release {RELEASE_TAG}"
        " (prerelease / technical preview)\n"
        " * Generated CSS; do not edit manually.\n"
        " * Chunk size: 256 codepoints.\n"
        " */\n\n"
    )
    body = "\n\n".join(r for _, _, r in all_rules)
    CSS_PATH.write_text(header + body + "\n", encoding="utf-8")
    print(f"\nCSS -> {CSS_PATH} ({len(all_rules)} @font-face rules)")


if __name__ == "__main__":
    main()

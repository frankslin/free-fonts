#!/usr/bin/env python3
"""Build chunked woff2 + CSS for the AR PL UKai webfont package.

Downloads the upstream ukai.ttc (文鼎PL中楷Uni, Arphic Public License) from the
Debian source tarball, slices each of its four faces (CN / TW / HK / TW MBE)
into 256-codepoint woff2 chunks, and generates arphic-ukai.css.

Usage:
    pip install fonttools brotli
    python3 build.py            # download to src/ + build all chunks
    python3 build.py --no-dl    # skip download (src/ukai.ttc already present)
    python3 build.py --jobs N   # explicit parallelism
"""

import argparse
import logging
import tarfile
import tempfile
import urllib.request
from multiprocessing import Pool, cpu_count
from pathlib import Path

from fontTools import subset as ft_subset
from fontTools.ttLib import TTFont

logging.getLogger("fontTools").setLevel(logging.ERROR)

ROOT = Path(__file__).parent
SRC_DIR = ROOT / "src"
FONTS_DIR = ROOT / "fonts"
CSS_PATH = ROOT / "arphic-ukai.css"
CHUNK_SIZE = 0x100

UPSTREAM_VERSION = "0.2.20080216.2"
TARBALL_URL = (
    "http://deb.debian.org/debian/pool/main/f/fonts-arphic-ukai/"
    f"fonts-arphic-ukai_{UPSTREAM_VERSION}.orig.tar.bz2"
)
TTC_NAME = "ukai.ttc"

# The four faces packed into ukai.ttc, in collection order.
SOURCES = [
    {"index": 0, "family": "AR PL UKai CN", "prefix": "ARPLUKaiCN", "weight": 400},
    {"index": 1, "family": "AR PL UKai HK", "prefix": "ARPLUKaiHK", "weight": 400},
    {"index": 2, "family": "AR PL UKai TW", "prefix": "ARPLUKaiTW", "weight": 400},
    {"index": 3, "family": "AR PL UKai TW MBE", "prefix": "ARPLUKaiTWMBE", "weight": 400},
]

# Arphic Public License 2(a): every modified file must carry a prominent notice
# stating how and when it was changed. Stamped into each woff2 chunk (name ID 10).
MOD_NOTICE = (
    "Modified for web use by the free-fonts project (2026): converted to WOFF2 "
    "and split into 256-codepoint subsets. Glyph outlines are unchanged. "
    "Sources: https://github.com/frankslin/free-fonts"
)


def download() -> None:
    SRC_DIR.mkdir(exist_ok=True)
    dest = SRC_DIR / TTC_NAME
    if dest.exists():
        print(f"{dest.name} already present, skipping download.")
        return
    print(f"Downloading {TARBALL_URL} ...")
    with tempfile.NamedTemporaryFile(suffix=".tar.bz2") as tmp:
        urllib.request.urlretrieve(TARBALL_URL, tmp.name)
        with tarfile.open(tmp.name) as tar:
            for member in tar.getmembers():
                if Path(member.name).name == TTC_NAME:
                    dest.write_bytes(tar.extractfile(member).read())
                    print(f"  {dest.stat().st_size / 1024 / 1024:.1f} MB -> {dest}")
                    return
    raise SystemExit(f"{TTC_NAME} not found in {TARBALL_URL}")


def _build_chunk(args: tuple) -> tuple[str, int]:
    ttc_path, font_number, cps, out_path = args
    options = ft_subset.Options()
    options.flavor = "woff2"
    options.name_IDs = [0, 1, 2, 4, 5, 10]
    options.font_number = font_number
    options.drop_tables += ["DSIG"]

    font = ft_subset.load_font(ttc_path, options)
    subsetter = ft_subset.Subsetter(options=options)
    subsetter.populate(unicodes=sorted(cps))
    subsetter.subset(font)
    font["name"].setName(MOD_NOTICE, 10, 3, 1, 0x409)
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
    ttc = SRC_DIR / TTC_NAME
    all_rules: list[tuple[int, int, str]] = []  # (face order, start, rule_text)

    for order, src in enumerate(SOURCES):
        weight = src["weight"]
        prefix = src["prefix"]
        tt = TTFont(str(ttc), lazy=True, fontNumber=src["index"])
        assert tt["name"].getDebugName(1) == src["family"], tt["name"].getDebugName(1)
        cps = set(tt.getBestCmap())
        version = tt["name"].getDebugName(5)
        tt.close()

        chunk_map: dict[int, set[int]] = {}
        for cp in cps:
            chunk_map.setdefault((cp // CHUNK_SIZE) * CHUNK_SIZE, set()).add(cp)
        print(f"{src['family']}: {len(cps):,} cps, {len(chunk_map)} chunks, {version}")

        tasks = [
            (str(ttc), src["index"], chunk_cps,
             str(FONTS_DIR / f"{prefix}-{weight}-{start:06x}.woff2"))
            for start, chunk_cps in sorted(chunk_map.items())
        ]
        with Pool(processes=args.jobs) as pool:
            for i, (name, size) in enumerate(pool.imap_unordered(_build_chunk, tasks), 1):
                if i % 40 == 0 or i == len(tasks):
                    print(f"  [{i}/{len(tasks)}] {name} {size // 1024} KB")

        for start in sorted(chunk_map):
            rule = (
                "@font-face {\n"
                f"  font-family: '{src['family']}';\n"
                "  font-style: normal;\n"
                f"  font-weight: {weight};\n"
                "  font-display: swap;\n"
                f"  src: url('fonts/{prefix}-{weight}-{start:06x}.woff2') format('woff2');\n"
                f"  unicode-range: {unicode_range_str(start)};\n"
                "}"
            )
            all_rules.append((order, start, rule))

    all_rules.sort(key=lambda x: (x[0], x[1]))
    header = (
        "/* AR PL UKai / 文鼎PL中楷Uni Webfonts (CN / HK / TW / TW MBE)\n"
        f" * Upstream: CJK Unifonts ukai.ttc {UPSTREAM_VERSION} (Arphic Public License)\n"
        " * Modified for web use: converted to WOFF2 and split into 256-codepoint\n"
        " * subsets; glyph outlines are unchanged.\n"
        " * Generated CSS; do not edit manually.\n"
        " */\n\n"
    )
    body = "\n\n".join(r for _, _, r in all_rules)
    CSS_PATH.write_text(header + body + "\n", encoding="utf-8")
    print(f"\nCSS -> {CSS_PATH} ({len(all_rules)} @font-face rules)")


if __name__ == "__main__":
    main()

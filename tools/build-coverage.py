#!/usr/bin/env python3
"""Generate assets/coverage-data.js — per-font Unicode / charset coverage counts.

Coverage is measured from the woff2 slices we actually ship: every @font-face
`src` in a package CSS is opened with fontTools and its cmap unioned per
variant. The CSS `unicode-range` is NOT used — a 256-codepoint chunk exists as
soon as it holds one glyph, so ranges would wildly overstate coverage.

Reference charsets come from two offline-ish sources:
  * Unihan (unicode.org, downloaded once into tools/.cache/) for the standard
    character lists: kTGH 通用规范汉字表, kIICore, kHKGlyph, kJoyoKanji, ...
  * Python's own codecs for the legacy encodings (GB/T 2312, GBK, Big5,
    Big5-HKSCS, JIS X 0208): a codepoint is in the charset iff it encodes.

Unicode block totals are hard-coded for the CJK ideograph blocks (contiguous
and fully assigned, so no unicodedata version skew — the stdlib's Unicode
version lags and would drop Ext-H/I) and derived via unicodedata elsewhere.

Usage:
    pip install fonttools brotli
    python3 tools/build-coverage.py            # all local packages
    python3 tools/build-coverage.py plangothic # one font id
"""

import io
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "tools", ".cache")
OUT = os.path.join(ROOT, "assets", "coverage-data.js")
UNIHAN_URL = "https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip"

# ── Unicode blocks ────────────────────────────────────────────────────────────
# full=True: contiguous, fully assigned (all CJK ideograph blocks) — counted as
# the whole range so the numbers stay right regardless of the stdlib's Unicode
# version. Everything else is counted by asking unicodedata what is assigned.
# group: "unicode" = 汉字相关区段, "other" = 其他区段.
BLOCKS = [
    ("radicals-sup", "汉字部首补充",           "CJK Radicals Supplement",  0x2E80, 0x2EF3, False, "unicode"),
    ("kangxi",       "康熙部首",               "Kangxi Radicals",          0x2F00, 0x2FD5, False, "unicode"),
    ("ids",          "表意文字描述符",         "Ideographic Description Characters", 0x2FF0, 0x2FFF, False, "unicode"),
    ("uro",          "中日韩统一表意文字",     "CJK Unified Ideographs",   0x4E00, 0x9FFF, True,  "unicode"),
    ("ext-a",        "统一表意文字扩展 A",     "CJK Ext-A",                0x3400, 0x4DBF, True,  "unicode"),
    ("compat",       "中日韩兼容表意文字",     "CJK Compatibility Ideographs", 0xF900, 0xFAFF, False, "unicode"),
    ("ext-b",        "统一表意文字扩展 B",     "CJK Ext-B",                0x20000, 0x2A6DF, True, "unicode"),
    ("ext-c",        "统一表意文字扩展 C",     "CJK Ext-C",                0x2A700, 0x2B739, True, "unicode"),
    ("ext-d",        "统一表意文字扩展 D",     "CJK Ext-D",                0x2B740, 0x2B81D, True, "unicode"),
    ("ext-e",        "统一表意文字扩展 E",     "CJK Ext-E",                0x2B820, 0x2CEA1, True, "unicode"),
    ("ext-f",        "统一表意文字扩展 F",     "CJK Ext-F",                0x2CEB0, 0x2EBE0, True, "unicode"),
    ("ext-i",        "统一表意文字扩展 I",     "CJK Ext-I",                0x2EBF0, 0x2EE5D, True, "unicode"),
    ("ext-g",        "统一表意文字扩展 G",     "CJK Ext-G",                0x30000, 0x3134A, True, "unicode"),
    ("ext-h",        "统一表意文字扩展 H",     "CJK Ext-H",                0x31350, 0x323AF, True, "unicode"),
    ("compat-sup",   "兼容表意文字补充",       "CJK Compat. Ideographs Sup.", 0x2F800, 0x2FA1D, True, "unicode"),
    ("latin",        "基本拉丁字母",           "Basic Latin",              0x0000, 0x007F, False, "other"),
    ("latin1",       "拉丁字母补充-1",         "Latin-1 Supplement",       0x0080, 0x00FF, False, "other"),
    ("cjk-punct",    "中日韩符号和标点",       "CJK Symbols and Punctuation", 0x3000, 0x303F, False, "other"),
    ("halfwidth",    "半角及全角形式",         "Halfwidth and Fullwidth Forms", 0xFF00, 0xFFEF, False, "other"),
    ("bopomofo",     "注音符号",               "Bopomofo",                 0x3100, 0x312F, False, "other"),
    ("bopomofo-ext", "注音符号扩展",           "Bopomofo Extended",        0x31A0, 0x31BF, False, "other"),
    ("hiragana",     "平假名",                 "Hiragana",                 0x3040, 0x309F, False, "other"),
    ("katakana",     "片假名",                 "Katakana",                 0x30A0, 0x30FF, False, "other"),
    ("hangul",       "谚文音节",               "Hangul Syllables",         0xAC00, 0xD7A3, True,  "other"),
]

# Blocks that make up the "汉字总数" tally.
IDEO_BLOCKS = ["uro", "ext-a", "compat", "ext-b", "ext-c", "ext-d", "ext-e",
               "ext-f", "ext-i", "ext-g", "ext-h", "compat-sup"]

# Unihan field -> row. (id, zh, en, file, field)
UNIHAN_LISTS = [
    ("tgh",      "通用规范汉字表 (2013)",   "Table of General Standard Chinese Characters", "Unihan_OtherMappings.txt", "kTGH"),
    ("iicore",   "国际表意文字核心 IICore", "IICore",                                       "Unihan_IRGSources.txt",    "kIICore"),
    ("core2020", "Unihan Core 2020",        "Unihan Core 2020",                             "Unihan_DictionaryLikeData.txt", "kUnihanCore2020"),
    ("hkglyph",  "常用字字形表 (香港)",     "HK List of Graphemes",                         "Unihan_DictionaryLikeData.txt", "kHKGlyph"),
    ("joyo",     "日本常用漢字",            "Japanese Jōyō Kanji",                          "Unihan_OtherMappings.txt", "kJoyoKanji"),
    ("jinmeiyo", "日本人名用漢字",          "Japanese Jinmeiyō Kanji",                      "Unihan_OtherMappings.txt", "kJinmeiyoKanji"),
    ("hanja",    "韩国教育用基础汉字",      "Korean Basic Hanja",                           "Unihan_OtherMappings.txt", "kKoreanEducationHanja"),
]

# Legacy encodings, counted over their 汉字 only (matches the numbers people
# know: GB/T 2312 = 6763, Big5 = 13060-ish).
ENCODINGS = [
    ("gb2312",    "GB/T 2312 汉字",      "GB/T 2312 hanzi",     "gb2312"),
    ("gbk",       "GBK 汉字",            "GBK hanzi",           "gbk"),
    ("big5",      "Big5 汉字",           "Big5 hanzi",          "big5"),
    ("big5hkscs", "Big5-HKSCS 汉字",     "Big5-HKSCS hanzi",    "big5hkscs"),
    ("jisx0208",  "JIS X 0208 漢字",     "JIS X 0208 kanji",    "shift_jis"),
]


def log(*a):
    print(*a, file=sys.stderr)


# ── charset construction ──────────────────────────────────────────────────────
def is_ideograph(cp):
    name = unicodedata.name(chr(cp), "")
    return name.startswith("CJK UNIFIED IDEOGRAPH") or name.startswith("CJK COMPATIBILITY IDEOGRAPH")


def block_set(start, end, full):
    if full:
        return set(range(start, end + 1))
    # Skip unassigned (Cn) and control characters (Cc) — no font maps C0/C1,
    # counting them would cap Basic Latin at 95/128 forever.
    return {cp for cp in range(start, end + 1)
            if unicodedata.category(chr(cp)) not in ("Cn", "Cc")}


def encoding_set(codec):
    out = set()
    for cp in range(0x110000):
        if 0xD800 <= cp < 0xE000:
            continue
        try:
            chr(cp).encode(codec)
        except Exception:
            continue
        out.add(cp)
    return out


def fetch_unihan():
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, "Unihan.zip")
    if not os.path.exists(path):
        log(f"downloading {UNIHAN_URL} …")
        with urllib.request.urlopen(UNIHAN_URL) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
    return zipfile.ZipFile(path)


def unihan_sets():
    zf = fetch_unihan()
    wanted = {}
    for cid, _zh, _en, fname, field in UNIHAN_LISTS:
        wanted.setdefault(fname, []).append((cid, field))
    out = {cid: set() for cid, *_ in UNIHAN_LISTS}
    for fname, fields in wanted.items():
        by_field = dict((f, c) for c, f in fields)
        with zf.open(fname) as fh:
            for line in io.TextIOWrapper(fh, "utf-8"):
                if not line.startswith("U+"):
                    continue
                cp_s, _, rest = line.partition("\t")
                field, _, _val = rest.partition("\t")
                cid = by_field.get(field)
                if cid:
                    out[cid].add(int(cp_s[2:], 16))
    return out


def build_charsets():
    """-> (groups[], sets{id: set[int]})"""
    sets = {}
    blocks = {"unicode": [], "other": []}
    for bid, zh, en, start, end, full, grp in BLOCKS:
        s = block_set(start, end, full)
        sets[bid] = s
        blocks[grp].append({"id": bid, "zh": zh, "en": en, "total": len(s),
                            "start": start, "end": end,
                            "range": f"U+{start:04X}–{end:04X}"})
    # 〇 is the odd one out: an ideographic digit outside every ideograph block.
    sets["ling"] = {0x3007}
    blocks["unicode"].insert([b["id"] for b in blocks["unicode"]].index("uro"),
                             {"id": "ling", "zh": "〇 (U+3007)", "en": "Ideographic number zero",
                              "total": 1, "start": 0x3007, "end": 0x3007, "range": "U+3007"})

    uh = unihan_sets()
    lists = []
    for cid, zh, en, _f, _k in UNIHAN_LISTS:
        sets[cid] = uh[cid]
        lists.append({"id": cid, "zh": zh, "en": en, "total": len(uh[cid])})

    encs = []
    for eid, zh, en, codec in ENCODINGS:
        s = {cp for cp in encoding_set(codec) if is_ideograph(cp)}
        sets[eid] = s
        encs.append({"id": eid, "zh": zh, "en": en, "total": len(s)})

    groups = [
        {"id": "unicode",   "zh": "汉字区段",     "en": "Unicode CJK blocks", "items": blocks["unicode"]},
        {"id": "standards", "zh": "字符集标准",   "en": "Legacy charsets",    "items": encs},
        {"id": "lists",     "zh": "常用字表",     "en": "Standard lists",     "items": lists},
        {"id": "other",     "zh": "其他区段",     "en": "Other blocks",       "items": blocks["other"]},
    ]
    return groups, sets


# ── font side ─────────────────────────────────────────────────────────────────
def load_fonts_data():
    js = os.path.join(ROOT, "assets", "fonts-data.js")
    code = f"""
      const fs=require('fs');
      const src=fs.readFileSync({json.dumps(js)},'utf8');
      const window={{}}; eval(src);
      process.stdout.write(JSON.stringify(window.FREE_FONTS_DATA));
    """
    out = subprocess.run(["node", "-e", code], capture_output=True, check=True)
    return json.loads(out.stdout)


FACE_RE = re.compile(r"@font-face\s*{([^}]*)}", re.S)


def css_faces(css_path):
    """-> list of (family, unicode_range, woff2_abs_path)"""
    with open(css_path, encoding="utf-8") as f:
        css = f.read()
    base = os.path.dirname(css_path)
    faces = []
    for body in FACE_RE.findall(css):
        fam = re.search(r"font-family:\s*([^;]+);", body)
        url = re.search(r"url\(['\"]?([^'\")]+)['\"]?\)", body)
        rng = re.search(r"unicode-range:\s*([^;]+);", body)
        if not url:
            continue
        faces.append((fam.group(1).strip() if fam else "",
                      rng.group(1).strip() if rng else "",
                      os.path.normpath(os.path.join(base, url.group(1)))))
    return faces


def cmap_of_css(css_paths):
    """Union of every slice's cmap, each file opened once."""
    from fontTools.ttLib import TTFont
    seen, cps, missing = set(), set(), 0
    for p in css_paths:
        for _fam, _rng, path in css_faces(p):
            if path in seen:
                continue
            seen.add(path)
            if not os.path.exists(path):
                missing += 1
                continue
            font = TTFont(path, lazy=True)
            cps.update(font.getBestCmap().keys())
            font.close()
    if missing:
        log(f"    ! {missing} slice(s) missing on disk")
    return cps


def main():
    only = set(sys.argv[1:])
    log("building charsets …")
    groups, sets = build_charsets()

    fonts = load_fonts_data()
    result = {}
    for font in fonts:
        fid = font["id"]
        if only and fid not in only:
            continue
        local = [os.path.join(ROOT, c[2:]) for c in font.get("css", []) if c.startswith("./")]
        if not local:
            log(f"{fid}: no local CSS, skipped")
            continue
        by_base = {os.path.basename(p): p for p in local}
        variants = {}
        for var in font["variants"]:
            pkgs = var.get("pkgs") or []
            paths = [by_base[p["css"]] for p in pkgs if p.get("css") in by_base]
            if not paths:
                paths = local  # single-CSS font whose variant carries no pkg
            cps = cmap_of_css(paths)
            counts = {}
            for gid, s in sets.items():
                n = len(cps & s)
                if n:
                    counts[gid] = n
            ideo = set()
            for bid in IDEO_BLOCKS:
                ideo |= sets[bid]
            ideo |= sets["ling"]
            variants[var["key"]] = {
                "glyphs": len(cps),
                "hanzi": len(cps & ideo),
                "hanziTotal": len(ideo),
                "counts": counts,
            }
            log(f"{fid}/{var['key']}: {len(cps)} cps, {variants[var['key']]['hanzi']} 汉字")
        result[fid] = variants

    payload = {
        "note": "Generated by tools/build-coverage.py; do not edit manually.",
        "unihanSource": UNIHAN_URL,
        "unicodeData": unicodedata.unidata_version,
        "groups": groups,
        "fonts": result,
    }
    if only and os.path.exists(OUT):  # partial rebuild: keep the other fonts
        with open(OUT, encoding="utf-8") as f:
            old = json.loads(f.read().split("=", 1)[1].rstrip().rstrip(";"))
        merged = old.get("fonts", {})
        merged.update(result)
        payload["fonts"] = merged

    # Emitted as a classic script (like assets/fonts-data.js) so both pages
    # keep working straight off file:// — fetch() of a .json would not.
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("/* Generated by tools/build-coverage.py; do not edit manually. */\n")
        f.write("window.FREE_FONTS_COVERAGE = ")
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    log(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()

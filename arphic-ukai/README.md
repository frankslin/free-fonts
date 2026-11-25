# AR PL UKai Webfonts

Chunked woff2 webfonts for AR PL UKai / 文鼎PL中楷Uni, generated from the CJK Unifonts `ukai.ttc` version 0.2.20080216.2.

AR PL UKai 是 Arne Goetje 與 [CJK Unifonts](https://www.freedesktop.org/wiki/Software/CJKUnifonts)
專案在文鼎PL中楷／簡中楷基礎上合併重製的 Unicode 版楷書：把 Big5 與 GB 2312 兩
套字集併入單一 Unicode 編碼，並補上 HKSCS-2004、注音擴充（客語／閩南語）與歐語
字母。TTC 內含四個 face，本 package 各自切成獨立的 webfont family：

| Family | 定位 | Codepoints |
| --- | --- | --- |
| `AR PL UKai CN` | zh_CN | 23,873 |
| `AR PL UKai HK` | zh_HK（多 2,614 個 HKSCS-2004 PUA 碼位） | 26,444 |
| `AR PL UKai TW` | zh_TW | 24,133 |
| `AR PL UKai TW MBE` | zh_TW，閩南語注音擴充用替代字形 | 24,090 |

**四個 face 的字形幾乎完全相同**，差異只在字集覆蓋，不在字形慣例。實測共有碼位
中：CN 與 TW 只有 `令`、`骨` 兩個字形不同；TW 與 HK 只差 `骨` 一個字；TW MBE 與
TW 只差 10 個注音擴充字母（U+31A0–31BF）的字形。上游 `KNOWN_ISSUES` 也寫明
"Only two glyphs available with different shapes for different flavors"。

對於陸／臺字形有分歧的字（如 `直`、`海`），四個 face 一律採用文鼎PL中楷（Big5）
的臺灣字形——包括 `AR PL UKai CN` 在內，**它並不是大陸字形的楷書**。實測 4,558
個「兩套經典字型字形不一致」的碼位中，UKai CN 沒有任何一個採用文鼎PL簡中楷的
輪廓。需要大陸字形楷書請改用 `@free-fonts/arphic-kaitim-gb`。

```html
<link rel="stylesheet" href="./arphic-ukai.css">
```

CDN：

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/arphic-ukai@1.0.0/arphic-ukai.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/arphic-ukai@1.0.0/arphic-ukai.css">
```

```css
body {
  font-family: 'AR PL UKai TW', cursive, serif;
}
```

The CSS uses 256-codepoint `unicode-range` chunks, so browsers only download the blocks needed by the page. 四個 family 名稱各自獨立，請依需要挑選，不要一次全部列進 fallback stack。

- 線上樣張 / Live specimen: <https://free-fonts.digitalhumanities.dev/specimen?font=arphic-ukai>
- Upstream: <https://www.freedesktop.org/wiki/Software/CJKUnifonts>（散布檔取自 <http://deb.debian.org/debian/pool/main/f/fonts-arphic-ukai/>）
- Upstream version: `0.2.20080216.2`
- Upstream font license: Arphic Public License（見 `LICENSE` 與 `ARPHICPL.TXT`）
- Package scripts and metadata license: MIT
- Generated woff2 files: 1,232

## 修改說明 / Modification notice

依 Arphic Public License 第 2(a) 條，本 package 於 2026 年將上游 `ukai.ttc` 的四
個 face 各自轉為 WOFF2 並依 256 codepoints 切片；字形輪廓未經更動，GSUB/GPOS 等
排版表保留。轉換用的 `build.py` 收錄於本 repo，重跑即可從上游重新產生。

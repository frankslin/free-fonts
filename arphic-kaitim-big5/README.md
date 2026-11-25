# AR PL KaitiM Big5 Webfonts

Chunked woff2 webfonts for AR PL KaitiM Big5 / 文鼎PL中楷, generated from the Arphic `bkai00mp.ttf` version 2.10.

文鼎PL中楷是文鼎科技 1999 年以 Arphic Public License 釋出的四套字型之一
（另有文鼎PL簡中楷、文鼎PL細上海宋、文鼎PL明體），長年是 Linux 桌面上的預設
中文楷書，字集對應 Big5。字重僅 Regular 一種。

```html
<link rel="stylesheet" href="./arphic-kaitim-big5.css">
```

CDN：

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/arphic-kaitim-big5@1.0.0/arphic-kaitim-big5.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/arphic-kaitim-big5@1.0.0/arphic-kaitim-big5.css">
```

```css
body {
  font-family: 'AR PL KaitiM Big5', cursive, serif;
}
```

The CSS uses 256-codepoint `unicode-range` chunks, so browsers only download the blocks needed by the page.

- 線上樣張 / Live specimen: <https://free-fonts.digitalhumanities.dev/specimen?font=arphic-kaitim>
- Upstream: <http://deb.debian.org/debian/pool/main/f/fonts-arphic-bkai00mp/> (Debian 保存的原始散布檔)
- Upstream version: `2.10`
- Upstream font license: Arphic Public License（見 `LICENSE` 與 `ARPHICPL.TXT`）
- Package scripts and metadata license: MIT
- Generated woff2 files: 101 (13,969 codepoints)

## 修改說明 / Modification notice

依 Arphic Public License 第 2(a) 條，本 package 於 2026 年將上游 `bkai00mp.ttf`
轉為 WOFF2 並依 256 codepoints 切片；字形輪廓未經更動，僅移除切片後失效的舊式
AAT `mort` 表。轉換用的 `build.py` 收錄於本 repo，重跑即可從上游重新產生。

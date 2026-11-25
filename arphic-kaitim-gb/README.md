# AR PL KaitiM GB Webfonts

Chunked woff2 webfonts for AR PL KaitiM GB / 文鼎PL簡中楷, generated from the Arphic `gkai00mp.ttf` version 2.11.

文鼎PL簡中楷是文鼎科技 1999 年以 Arphic Public License 釋出的四套字型之一
（另有文鼎PL中楷、文鼎PL細上海宋、文鼎PL明體），長年是 Linux 桌面上的預設中文
楷書，字集對應 GB 2312-80。字重僅 Regular 一種。

```html
<link rel="stylesheet" href="./arphic-kaitim-gb.css">
```

CDN：

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/arphic-kaitim-gb@1.0.0/arphic-kaitim-gb.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/arphic-kaitim-gb@1.0.0/arphic-kaitim-gb.css">
```

```css
body {
  font-family: 'AR PL KaitiM GB', cursive, serif;
}
```

The CSS uses 256-codepoint `unicode-range` chunks, so browsers only download the blocks needed by the page.

- 線上樣張 / Live specimen: <https://free-fonts.digitalhumanities.dev/specimen?font=arphic-kaitim>
- Upstream: <http://deb.debian.org/debian/pool/main/f/fonts-arphic-gkai00mp/> (Debian 保存的原始散布檔)
- Upstream version: `2.11`
- Upstream font license: Arphic Public License（見 `LICENSE` 與 `ARPHICPL.TXT`）
- Package scripts and metadata license: MIT
- Generated woff2 files: 98 (7,574 codepoints)

## 修改說明 / Modification notice

依 Arphic Public License 第 2(a) 條，本 package 於 2026 年將上游 `gkai00mp.ttf`
轉為 WOFF2 並依 256 codepoints 切片；字形輪廓未經更動，僅移除切片後失效的舊式
AAT `mort` 表。轉換用的 `build.py` 收錄於本 repo，重跑即可從上游重新產生。

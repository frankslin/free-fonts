# TW-Sung Webfonts

Chunked woff2 webfonts for TW-Sung / 全字庫正宋體, generated from CNS11643 中文標準交換碼全字庫 2026-05-05.

```html
<link rel="stylesheet" href="./tw-sung.css">
```

```css
body {
  font-family: 'TW-Sung', serif;
}
```

The CSS uses 256-codepoint `unicode-range` chunks, so browsers only download the blocks needed by the page. The package combines the upstream BMP, Ext-B, and Plus TTF faces into one CSS family with first-seen codepoint deduplication.

- 線上樣張 / Live specimen: <https://free-fonts.digitalhumanities.dev/specimen?font=tw-sung>
- Upstream: https://data.gov.tw/dataset/5961
- Upstream version: `2026-05-05`
- Upstream font license: SIL Open Font License 1.1 (the dataset also allows Government Open Data License 1.0 as an alternative)
- Package scripts and metadata license: MIT
- Generated woff2 files: 530
- Unique codepoints: 113646

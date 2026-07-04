# free-fonts

**The missing webfonts for your SIL releases**

`free-fonts` 將適合中文排版、且可自由再散布的字型整理成可直接引用的
webfont packages。每套字型都切成 256 codepoints 一片的 WOFF2 檔案，並以
CSS `unicode-range` 宣告，讓瀏覽器只下載頁面實際需要的字元區塊。

## 目前包含

- `@free-fonts/genki-mincho`：源起明體 TC webfont。
- `@free-fonts/genyo-mincho`：源樣明體 TC webfont。
- `@free-fonts/wenjin-mincho`：文津明體 Plane 0、Plane 2、Plane 3 webfont。

根目錄的 `index.html` 是互動式展示頁，可比較各字型、系統 fallback、繁簡轉換
與單字形差異。

## 使用方式

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/wenjin-mincho@1.0.0/wenjin-mincho.css">
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/genki-mincho@1.0.0/genki-mincho.css">
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/genyo-mincho@1.0.0/genyo-mincho.css">
```

```css
.wenjin {
  font-family: "WenJin Mincho Plane 0", "WenJin Mincho Plane 2",
    "WenJin Mincho Plane 3", serif;
}

.genki {
  font-family: "GenKiMin2TC", serif;
}

.genyo {
  font-family: "GenYoMin2TC", serif;
}
```

## 切片原則

- 每片涵蓋 `0x100` 個 codepoints，對齊 Google Noto CJK 常見做法。
- CSS 以 `@font-face` 加 `unicode-range` 精準描述每片覆蓋範圍。
- package 內保留原字型家族名稱，避免使用者需要記憶額外 fallback 名稱。
- 每個字型 package 都包含自己的 `package.json`、CSS 與 `fonts/*.woff2`。

## 授權

本 repo 的包裝檔、展示頁與建置腳本以 MIT 授權釋出。各字型本身依原作者授權
釋出；目前 packages 使用 `MIT+SIL-1.1` 標示，以反映包裝程式碼與字型授權的組合。

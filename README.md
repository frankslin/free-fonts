# free-fonts

**The missing webfonts for your SIL free-font releases**

`free-fonts` 將適合中文排版、且可自由再散布的字型整理成可直接引用的
webfont packages。每套字型都切成 256 codepoints 一片的 WOFF2 檔案，並以
CSS `unicode-range` 宣告，讓瀏覽器只下載頁面實際需要的字元區塊。

* 中文網頁內嵌字型大比拼： https://free-fonts.digitalhumanities.dev/

## 目前包含

目前包含：文津明體、源起明體 TC、源樣明體 TC、黑糖话梅、霞鹜文楷、霞鹜文楷 GB、霞鶩文楷 TC。

根目錄的 `index.html` 是互動式展示頁，可比較各字型、系統 fallback、繁簡轉換
與單字形差異。

## 使用方式

### 文津明體

來源：[takushun-wu/WenJinMincho](https://github.com/takushun-wu/WenJinMincho)。文津明體是覆蓋面廣的開源明體，採用中國字型習慣，本 package 使用其 Plane 0、Plane 2、Plane 3 標準 OTF 分件。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/wenjin-mincho@1.0.0/wenjin-mincho.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/wenjin-mincho@1.0.0/wenjin-mincho.css">
```

```css
.wenjin {
  font-family: "WenJin Mincho Plane 0", "WenJin Mincho Plane 2",
    "WenJin Mincho Plane 3", serif;
}
```

### 源起明體 TC

來源：[ButTaiwan/genyo-font](https://github.com/ButTaiwan/genyo-font)。源起明體是 But Ko 基於思源宋體衍生的傳統中文明體系列，這裡打包 TC 版本。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/genki-mincho@1.0.0/genki-mincho.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/genki-mincho@1.0.0/genki-mincho.css">
```

```css
.genki {
  font-family: "GenKiMin2TC", serif;
}
```

### 源樣明體 TC

來源：[ButTaiwan/genyo-font](https://github.com/ButTaiwan/genyo-font)。源樣明體是 But Ko 基於思源宋體衍生的傳統中文明體系列，這裡打包 TC 版本。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/genyo-mincho@1.0.0/genyo-mincho.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/genyo-mincho@1.0.0/genyo-mincho.css">
```

```css
.genyo {
  font-family: "GenYoMin2TC", serif;
}
```

### 霞鹜文楷

來源：[lxgw/LxgwWenKai](https://github.com/lxgw/LxgwWenKai)，上游版本：`v1.522`。霞鹜文楷源自 Fontworks 的 Klee One，由 LXGW 補全簡體中文常用字與符號，形成適合中文排版的開源文楷。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/lxgw-wenkai@1.0.0/lxgw-wenkai.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/lxgw-wenkai@1.0.0/lxgw-wenkai.css">
```

```css
.lxgw-wenkai {
  font-family: "LXGW WenKai", cursive, sans-serif;
}
```

可使用 `font-weight: 300`、`400`、`500` 選擇 Light、Regular、Medium。

### 霞鹜文楷 GB

來源：[lxgw/LxgwWenKaiGB](https://github.com/lxgw/LxgwWenKaiGB)，上游版本：`v1.522`。霞鹜文楷 GB 是霞鹜文楷面向简体中文标准字形的版本，展示页会把它作为简体中文（SC）variant 使用；不带后缀的 LXGW WenKai 保留给英文界面展示。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/lxgw-wenkai-gb@1.0.0/lxgw-wenkai-gb.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/lxgw-wenkai-gb@1.0.0/lxgw-wenkai-gb.css">
```

```css
.lxgw-wenkai-gb {
  font-family: "LXGW WenKai GB", cursive, sans-serif;
}
```

可使用 `font-weight: 300`、`400`、`500` 選擇 Light、Regular、Medium。

### 霞鶩文楷 TC

來源：[lxgw/LxgwWenkaiTC](https://github.com/lxgw/LxgwWenkaiTC)，上游版本：`v1.522`。霞鶩文楷 TC 是 LXGW WenKai 的傳統中文版本，延續 Klee One 的文楷風格並調整補全繁體中文用字。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/lxgw-wenkai-tc@1.0.0/lxgw-wenkai-tc.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/lxgw-wenkai-tc@1.0.0/lxgw-wenkai-tc.css">
```

```css
.lxgw-wenkai-tc {
  font-family: "LXGW WenKai TC", cursive, sans-serif;
}
```

可使用 `font-weight: 300`、`400`、`500` 選擇 Light、Regular、Medium。

### 黑糖话梅

來源：[lxgw/BlackSugarPlumCandy](https://github.com/lxgw/BlackSugarPlumCandy)。黑糖话梅是 LXGW 以多款 OFL 開源字型融合製作的可愛風格字型，本 package 使用其 Bold TTF。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/black-sugar-plum-candy@1.0.0/black-sugar-plum-candy.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/black-sugar-plum-candy@1.0.0/black-sugar-plum-candy.css">
```

```css
.black-sugar-plum-candy {
  font-family: "Black Sugar Plum Candy", sans-serif;
  font-weight: 700;
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

# free-fonts

**The missing webfonts for your SIL free-font releases**

`free-fonts` 將適合中文排版、且可自由再散布的字型整理成可直接引用的
webfont packages。每套字型都切成 256 codepoints 一片的 WOFF2 檔案，並以
CSS `unicode-range` 宣告，讓瀏覽器只下載頁面實際需要的字元區塊。

* 中文網頁內嵌字型大比拼： https://free-fonts.digitalhumanities.dev/

## 目前包含

目前包含：文津明體、源起明體 TC、源樣明體 TC、全字庫正宋體、全字庫正楷體、黑糖话梅、霞鹜文楷、霞鹜文楷 GB、霞鶩文楷 TC、霞鶩975圓體 SC、霞鶩漫黑、遍黑體、BabelStone Han（巴貝斯通漢，submodule）、朱雀仿宋（prerelease）、文鼎PL中楷（Big5）、文鼎PL簡中楷（GB）、文鼎PL中楷Uni（AR PL UKai，CN／HK／TW／TW MBE）、開元楷體 SC（Kaiyuan Kai SC，submodule）。

根目錄的 `index.html` 是互動式展示頁，可比較各字型、系統 fallback、繁簡轉換
與單字形差異；`specimen.html?font=<id>` 是單字型樣張（含字符覆蓋表與 glyph
browser）；`coverage.html` 是各字型的覆蓋率橫向對照表；`arphic-compare.html` 是文鼎
三個 package（簡中楷／中楷／UKai 四個 face）的逐字形對照表，可依「陸臺分歧字」等
視角篩選，並標出哪幾個 face 的輪廓其實完全相同。

## 使用方式

### 文津明體

來源：[takushun-wu/WenJinMincho](https://github.com/takushun-wu/WenJinMincho)。文津明體是覆蓋面廣的開源明體，採用中國字型習慣，本 package 使用其 Plane 0、Plane 2、Plane 3 標準 OTF 分件。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/wenjin-mincho@1.0.1/wenjin-mincho.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/wenjin-mincho@1.0.1/wenjin-mincho.css">
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
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/genki-mincho@1.0.1/genki-mincho.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/genki-mincho@1.0.1/genki-mincho.css">
```

```css
.genki {
  font-family: "GenKiMin2TC", serif;
}
```

### 源樣明體 TC

來源：[ButTaiwan/genyo-font](https://github.com/ButTaiwan/genyo-font)。源樣明體是 But Ko 基於思源宋體衍生的傳統中文明體系列，這裡打包 TC 版本。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/genyo-mincho@1.0.1/genyo-mincho.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/genyo-mincho@1.0.1/genyo-mincho.css">
```

```css
.genyo {
  font-family: "GenYoMin2TC", serif;
}
```

### 全字庫正宋體

來源：[CNS11643中文標準交換碼全字庫](https://data.gov.tw/dataset/5961)，上游版本：`2026-05-05`。全字庫由數位發展部提供，正宋體對應 CNS11643/Unicode 字面，這裡將 BMP、Ext-B、Plus 三份 TTF 合成單一 `TW-Sung` webfont family。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/tw-sung@1.0.1/tw-sung.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/tw-sung@1.0.1/tw-sung.css">
```

```css
.tw-sung {
  font-family: "TW-Sung", serif;
}
```

### 全字庫正楷體

來源：[CNS11643中文標準交換碼全字庫](https://data.gov.tw/dataset/5961)，上游版本：`2026-05-05`。全字庫正楷體是臺灣 CNS11643 全字庫公開字型之一，這裡將 BMP、Ext-B、Plus 三份 TTF 合成單一 `TW-Kai` webfont family。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/tw-kai@1.0.1/tw-kai.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/tw-kai@1.0.1/tw-kai.css">
```

```css
.tw-kai {
  font-family: "TW-Kai", cursive, serif;
}
```

### 霞鹜文楷

來源：[lxgw/LxgwWenKai](https://github.com/lxgw/LxgwWenKai)，上游版本：`v1.522`。霞鹜文楷源自 Fontworks 的 Klee One，由 LXGW 補全簡體中文常用字與符號，形成適合中文排版的開源文楷。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/lxgw-wenkai@1.0.1/lxgw-wenkai.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/lxgw-wenkai@1.0.1/lxgw-wenkai.css">
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
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/lxgw-wenkai-gb@1.0.1/lxgw-wenkai-gb.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/lxgw-wenkai-gb@1.0.1/lxgw-wenkai-gb.css">
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
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/lxgw-wenkai-tc@1.0.1/lxgw-wenkai-tc.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/lxgw-wenkai-tc@1.0.1/lxgw-wenkai-tc.css">
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
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/black-sugar-plum-candy@1.0.1/black-sugar-plum-candy.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/black-sugar-plum-candy@1.0.1/black-sugar-plum-candy.css">
```

```css
.black-sugar-plum-candy {
  font-family: "Black Sugar Plum Candy", sans-serif;
  font-weight: 700;
}
```

### 朱雀仿宋

來源：[TrionesType/zhuque](https://github.com/TrionesType/zhuque)。朱雀仿宋是開源仿宋體計畫，本 package 使用其 v0.212 發布版。**注意：上游 v0.212 為 prerelease 版（字體內部標註 technical preview），字符覆蓋與字形在後續版本可能變動。**

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/zhuque-fangsong@1.0.0/zhuque-fangsong.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/zhuque-fangsong@1.0.0/zhuque-fangsong.css">
```

```css
.zhuque {
  font-family: "Zhuque Fangsong", serif;
}
```

### 文鼎PL中楷 / 文鼎PL簡中楷

來源：文鼎科技 1999 年以 [Arphic Public License](arphic-kaitim-big5/ARPHICPL.TXT) 釋出的 `bkai00mp.ttf`（Big5，上游版本 `2.10`）與 `gkai00mp.ttf`（GB 2312，上游版本 `2.11`），散布檔取自 Debian 保存的原始 tarball。這兩套是長年 Linux 桌面上的預設中文楷書。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/arphic-kaitim-big5@1.0.0/arphic-kaitim-big5.css">
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/arphic-kaitim-gb@1.0.0/arphic-kaitim-gb.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/arphic-kaitim-big5@1.0.0/arphic-kaitim-big5.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/arphic-kaitim-gb@1.0.0/arphic-kaitim-gb.css">
```

```css
.arphic-kaitim {
  font-family: "AR PL KaitiM Big5", cursive, serif;
}

.arphic-kaitim-gb {
  font-family: "AR PL KaitiM GB", cursive, serif;
}
```

### 文鼎PL中楷Uni（AR PL UKai）

來源：[CJK Unifonts](https://www.freedesktop.org/wiki/Software/CJKUnifonts) 的 `ukai.ttc`，上游版本：`0.2.20080216.2`。Arne Goetje 在文鼎PL中楷／簡中楷基礎上合併重製的 Unicode 版楷書，補上 HKSCS-2004、注音擴充與歐語字母，一個 TTC 內含 CN、HK、TW、TW MBE 四個 face，本 package 各自成為獨立 family。注意四個 face 的**字形幾乎相同**（CN 與 TW 只差 `令`、`骨` 兩字），差別在字集覆蓋；陸／臺字形分歧的字一律取臺灣字形，需要大陸字形楷書請用文鼎PL簡中楷。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/arphic-ukai@1.0.0/arphic-ukai.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/arphic-ukai@1.0.0/arphic-ukai.css">
```

```css
.arphic-ukai {
  font-family: "AR PL UKai TW", cursive, serif; /* 或 CN / HK / TW MBE */
}
```

### 開元楷體 SC（Kaiyuan Kai SC）

來源：[daizhige-org/kaiyuan-kai](https://github.com/daizhige-org/kaiyuan-kai)（submodule）。面向簡體中文的合併楷體：文鼎PL簡中楷（`gkai00mp.ttf`）有的碼位一律取簡中楷的大陸字形，其餘碼位以 AR PL UKai 的 CN face 補齊，共 23,875 碼位；另修正了破折號／省略號接續、標點縱向位置與垂直度量，並新增 `halt` 半寬標點特性。修改說明見該 package 的 `README.md`。

```html
<link rel="stylesheet" href="https://unpkg.com/@free-fonts/kaiyuan-kai-sc@0.0.1/kaiyuan-kai-sc.css">
```

jsDelivr 等效：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@free-fonts/kaiyuan-kai-sc@0.0.1/kaiyuan-kai-sc.css">
```

```css
.kaiyuan-kai {
  font-family: "Kaiyuan Kai SC", cursive, serif;
}
```

## 切片原則

- 每片涵蓋 `0x100` 個 codepoints，對齊 Google Noto CJK 常見做法。
- CSS 以 `@font-face` 加 `unicode-range` 精準描述每片覆蓋範圍。
- package 內保留原字型家族名稱，避免使用者需要記憶額外 fallback 名稱。
- 每個字型 package 都包含自己的 `package.json`、CSS 與 `fonts/*.woff2`。

## 授權

本 repo 的包裝檔、展示頁與建置腳本以 MIT 授權釋出。各字型本身依原作者授權
釋出；多數 packages 使用 `MIT AND OFL-1.1` 標示，以反映包裝程式碼與字型授權的組合。全字庫 package 依資料集提供的選項採用 OFL-1.1 散布字型。文鼎的三個 package
（`arphic-kaitim-big5`、`arphic-kaitim-gb`、`arphic-ukai`）與由其合併衍生的
`kaiyuan-kai-sc` 字型部分為 Arphic
Public License，標示為 `MIT AND Arphic-1999`；依該授權第 2(a) 條，切片轉檔的
修改說明列於各 package 的 `LICENSE` 與 `README.md`，授權原文另以 `ARPHICPL.TXT`
原樣附上。

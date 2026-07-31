# AGENTS.md

## 這個 repo 是什麼

`free-fonts` 把可自由再散布的中文字型（SIL OFL 等授權）打包成可直接經 CDN 引用的
npm webfont packages（`@free-fonts/*` scope）。每套字型被切成 **256 codepoints
（0x100）一片**的 WOFF2 檔案，CSS 用 `unicode-range` 宣告，瀏覽器只下載頁面實際
用到的區塊。展示站：https://free-fonts.digitalhumanities.dev/

## 目錄結構

- 根目錄下每個字型一個資料夾（`plangothic/`、`lxgw-wenkai/`、`tw-kai/` …），
  每個資料夾就是一個獨立的 npm package。
- `BabelStoneHan-UFO-Fonts/` 與 `zhuque-fangsong/` 是 **git submodules**（指向
  free-fonts-npm org 下的同名 repo），結構與其他 package 相同，但改動要在
  submodule 自己的 repo 裡 commit，再回主 repo bump 指針。新 package 傾向走這條
  路線（字體不常發版，獨立 repo 可獨立更新，主 repo 不用累積所有字體的全部版本
  歷史）；submodule package 的 `package.json` repository 欄位指向自己的 repo，
  不帶 `directory`。
- `index.html` — 互動式字型比較頁（比較各字型、系統 fallback、繁簡轉換、單字形差異）。
- `specimen.html` — 單字型樣張頁（`specimen.html?font=<id>`），含 type tester 與
  glyph browser。
- `assets/fonts-data.js` — **兩個頁面共用的字型 metadata**（classic script，
  暴露 `window.FREE_FONTS_DATA`，schema 見檔案開頭註解）。
- 兩個 HTML 頁面都是無 build step 的單檔頁面，直接以 `file://` 打開即可測試。

## 單一 package 的組成

```
<font>/
  build.py        # 產生器：下載上游 TTF → 切片 → 產出 fonts/*.woff2 + <font>.css
  src/            # 上游原始 TTF，被 .gitignore 排除，不入版控
  fonts/          # 切片後的 woff2，**有 commit**（CDN 直接吃 repo/npm 內容）
  <font>.css      # 產生的 CSS，檔頭標明 "Generated CSS; do not edit manually."
  package.json    # name=@free-fonts/<font>，main/style 指向 CSS，files 含 css/fonts/README/LICENSE
  README.md       # 使用方式（unpkg + jsDelivr 兩種 <link>）、來源、specimen 連結
  LICENSE         # 上游授權；license 欄位常見 "MIT AND OFL-1.1"（打包腳本 MIT、字型 OFL）
```

早期的 package（如 `tw-kai`、`lxgw-wenkai`）沒有 `build.py`；新 package 一律要有。

## 慣例

- 切片檔名：`<Prefix>-<weight>-<起始碼位六位十六進位>.woff2`，
  例 `PlangothicP1-400-000300.woff2`（覆蓋 U+0300–03FF）。
- `@font-face` 一律 `font-display: swap`。
- 不要手改任何 `<font>.css` —— 改 `build.py` 後重跑。
- 新 `build.py` 直接拷貝最近的一個（如 `plangothic/build.py` 或
  `lxgw-975-yuan/build.py`）改參數：上游 release URL、SOURCES、FAMILY、weight。
  需要保留 OpenType layout / IVS 的字型參考 `BabelStoneHan-UFO-Fonts/build.py`
  （`keep_layout`、variation selectors 處理）。
- build 依賴：`pip install fonttools brotli`；`python3 build.py`（`--no-dl` 跳過下載）。
- 版本號進 README 的 CDN URL 與 `assets/fonts-data.js` 的 `pkgs[].version`，
  發新版時三處要同步。

## 新增一套字型的 checklist

1. 建 `<font>/`：`build.py`（含 `.gitignore` 排除 `src/`）、跑出 `fonts/` 與 CSS。
2. `package.json`（scope `@free-fonts/`，repository.directory 指向子目錄）、
   `README.md`（unpkg + jsDelivr 用法、來源、specimen 連結）、`LICENSE`。
3. 在 `assets/fonts-data.js` 註冊（id、nameEn/nameZh、css、upstream、license、
   variants；schema 註解在檔頭）。
4. 確認 `index.html` 與 `specimen.html` 都能顯示（兩頁都吃 fonts-data.js，
   但 index 可能還需要 per-font 的調整，如 `autoByLang`）。
5. 更新根目錄 `README.md` 的「目前包含」清單與使用方式章節。
6. commit 訊息風格參考 git log：英文祈使句，如
   `Add plangothic webfont package (@free-fonts/plangothic v1.0.0)`。

## 注意

- `fonts/` 內動輒數百個 woff2（repo 已 commit 一萬多個），避免無謂的全量重跑或
  批次改名；diff 會非常大。
- 頁面語言混用繁簡（README 繁體為主）；UI 文案與字型名稱注意繁簡對應
  （fonts-data.js 有 nameZh/shortZh 區分）。

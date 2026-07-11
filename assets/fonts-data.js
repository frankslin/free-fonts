/*
 * Shared font metadata for index.html and specimen.html.
 * Loaded as a classic script (works over file://), exposes window.FREE_FONTS_DATA.
 *
 * Schema per font:
 *   id           stable id, shared across both pages (specimen.html?font=<id>)
 *   nameEn/nameZh   full names (specimen header)
 *   shortEn/shortZh optional shorter names used by index toggles/cards
 *   displayText  large sample text on the specimen header
 *   css          stylesheet hrefs loaded on demand (relative to repo root, or absolute URL)
 *   upstream     upstream project URL
 *   license      license name; licenseNote for extra restrictions
 *   noCdns       CDN tabs to hide on the specimen usage section (e.g. ["jsdelivr"])
 *   autoByLang   index-only: lang -> index variant key for the "Auto" option
 *   flattenWeightsInIndex  index-only: expand each weight into its own variant
 *                (keys become "<key>-light|regular|medium|semibold|bold")
 *   variants[]   { key, label, family, stack, weights[], pkgs?[{name,version,css}] }
 *                stack is the short human-readable family list shown on index cards
 */
window.FREE_FONTS_DATA = [
  {
    id: "wenjin",
    nameEn: "WenJin Mincho",
    nameZh: "文津明朝",
    displayText: "文津明朝",
    css: ["./wenjin-mincho/wenjin-mincho.css"],
    upstream: "https://github.com/takushun-wu/WenJinMincho",
    license: "SIL OFL 1.1",
    variants: [
      { key: "default", label: "Default", family: '"WenJin Mincho Plane 0","WenJin Mincho Plane 2","WenJin Mincho Plane 3",serif',
        stack: "WenJin Mincho Plane 0, 2, 3", weights: [400],
        pkgs: [{ name: "@free-fonts/wenjin-mincho", version: "1.0.1", css: "wenjin-mincho.css" }] }
    ]
  },
  {
    id: "genki",
    nameEn: "Genki Mincho",
    nameZh: "源起明體 TC",
    shortZh: "源起明體",
    displayText: "源起明體",
    css: ["./genki-mincho/genki-mincho.css"],
    upstream: "https://github.com/ButTaiwan/genyo-font",
    license: "SIL OFL 1.1",
    variants: [
      { key: "default", label: "TC", family: '"GenKiMin2TC",serif', stack: "GenKiMin2TC", weights: [400],
        pkgs: [{ name: "@free-fonts/genki-mincho", version: "1.0.1", css: "genki-mincho.css" }] }
    ]
  },
  {
    id: "genyo",
    nameEn: "GenYo Mincho",
    nameZh: "源樣明體 TC",
    shortZh: "源樣明體",
    displayText: "源樣明體",
    css: ["./genyo-mincho/genyo-mincho.css"],
    upstream: "https://github.com/ButTaiwan/genyo-font",
    license: "SIL OFL 1.1",
    variants: [
      { key: "default", label: "TC", family: '"GenYoMin2TC",serif', stack: "GenYoMin2TC", weights: [400],
        pkgs: [{ name: "@free-fonts/genyo-mincho", version: "1.0.1", css: "genyo-mincho.css" }] }
    ]
  },
  {
    id: "black-sugar-plum-candy",
    nameEn: "Black Sugar Plum Candy",
    nameZh: "黑糖话梅",
    displayText: "黑糖话梅",
    css: ["./black-sugar-plum-candy/black-sugar-plum-candy.css"],
    upstream: "https://github.com/lxgw/BlackSugarPlumCandy",
    license: "SIL OFL 1.1",
    variants: [
      { key: "default", label: "Bold", family: '"Black Sugar Plum Candy",sans-serif',
        stack: "Black Sugar Plum Candy", weights: [700],
        pkgs: [{ name: "@free-fonts/black-sugar-plum-candy", version: "1.0.1", css: "black-sugar-plum-candy.css" }] }
    ]
  },
  {
    id: "lxgw-wenkai",
    nameEn: "LXGW WenKai",
    nameZh: "霞鶩文楷",
    displayText: "霞鶩文楷",
    css: ["./lxgw-wenkai/lxgw-wenkai.css", "./lxgw-wenkai-gb/lxgw-wenkai-gb.css", "./lxgw-wenkai-tc/lxgw-wenkai-tc.css"],
    upstream: "https://github.com/lxgw/LxgwWenKai",
    license: "SIL OFL 1.1",
    flattenWeightsInIndex: true,
    autoByLang: { "zh-Hans": "gb-regular", "zh-Hant": "tc-regular", en: "original-regular" },
    variants: [
      { key: "original", label: "Original", family: '"LXGW WenKai",cursive,sans-serif',
        stack: "LXGW WenKai", weights: [300, 400, 500],
        pkgs: [{ name: "@free-fonts/lxgw-wenkai", version: "1.0.1", css: "lxgw-wenkai.css" }] },
      { key: "gb", label: "GB", family: '"LXGW WenKai GB",cursive,sans-serif',
        stack: "LXGW WenKai GB", weights: [300, 400, 500],
        pkgs: [{ name: "@free-fonts/lxgw-wenkai-gb", version: "1.0.1", css: "lxgw-wenkai-gb.css" }] },
      { key: "tc", label: "TC", family: '"LXGW WenKai TC",cursive,sans-serif',
        stack: "LXGW WenKai TC", weights: [300, 400, 500],
        pkgs: [{ name: "@free-fonts/lxgw-wenkai-tc", version: "1.0.1", css: "lxgw-wenkai-tc.css" }] }
    ]
  },
  {
    id: "tw-sung",
    nameEn: "TW-Sung",
    nameZh: "全字庫正宋體",
    displayText: "全字庫正宋體",
    css: ["./tw-sung/tw-sung.css"],
    upstream: "https://data.gov.tw/dataset/5961",
    license: "全字庫 OFL",
    variants: [
      { key: "default", label: "Regular", family: '"TW-Sung",serif', stack: "TW-Sung", weights: [400],
        pkgs: [{ name: "@free-fonts/tw-sung", version: "1.0.0", css: "tw-sung.css" }] }
    ]
  },
  {
    id: "tw-kai",
    nameEn: "TW-Kai",
    nameZh: "全字庫正楷體",
    displayText: "全字庫正楷體",
    css: ["./tw-kai/tw-kai.css"],
    upstream: "https://data.gov.tw/dataset/5961",
    license: "全字庫 OFL",
    variants: [
      { key: "default", label: "Regular", family: '"TW-Kai",cursive,serif', stack: "TW-Kai", weights: [400],
        pkgs: [{ name: "@free-fonts/tw-kai", version: "1.0.0", css: "tw-kai.css" }] }
    ]
  },
  {
    id: "wfg-fsung",
    nameEn: "WFG FSung",
    nameZh: "WFG 全宋體",
    displayText: "全宋體",
    css: ["https://unpkg.com/wfg-fsung-webfonts@1.0.1/wfg-fsung.css"],
    upstream: "https://www.npmjs.com/package/wfg-fsung-webfonts",
    license: "WFG NonCommercial",
    licenseNote: "非商業用途限定（學術研究、教育、個人閱讀），禁止用於商業盈利",
    noCdns: ["jsdelivr"],
    variants: [
      { key: "default", label: "Regular", family: "'WFG FSung', serif", stack: "WFG FSung", weights: [400],
        pkgs: [{ name: "wfg-fsung-webfonts", version: "1.0.1", css: "wfg-fsung.css" }] }
    ]
  },
  {
    id: "babelstone-han",
    nameEn: "BabelStone Han",
    nameZh: "巴貝斯通漢",
    displayText: "漢字大全",
    css: ["./BabelStoneHan-UFO-Fonts/babelstone-han.css"],
    upstream: "https://github.com/babelstone/babelstonehan-ufo",
    license: "Arphic 1999",
    variants: [
      { key: "default", label: "Default", family: "'BabelStone Han Basic','BabelStone Han Extra','BabelStone Han PUA',serif",
        stack: "BabelStone Han Basic/Extra/PUA", weights: [400],
        pkgs: [{ name: "@free-fonts/babelstone-han", version: "1.0.0", css: "babelstone-han.css" }] }
    ]
  },
  {
    id: "lxgw-975-yuan",
    nameEn: "LXGW 975 Yuan SC",
    nameZh: "霞鶩975圓體SC",
    displayText: "霞鶩975圓體",
    css: ["./lxgw-975-yuan/lxgw-975-yuan.css"],
    upstream: "https://github.com/lxgw/975Yuan",
    license: "SIL OFL 1.1",
    variants: [
      { key: "default", label: "Regular", family: "'LXGW 975 Yuan SC',sans-serif",
        stack: "LXGW 975 Yuan SC", weights: [400, 500, 700],
        pkgs: [{ name: "@free-fonts/lxgw-975-yuan", version: "1.0.0", css: "lxgw-975-yuan.css" }] }
    ]
  },
  {
    id: "lxgw-marker-gothic",
    nameEn: "LXGW Marker Gothic",
    nameZh: "霞鶩漫黑",
    displayText: "霞鶩漫黑",
    css: ["./lxgw-marker-gothic/lxgw-marker-gothic.css"],
    upstream: "https://github.com/lxgw/LxgwMarkerGothic",
    license: "SIL OFL 1.1",
    variants: [
      { key: "default", label: "Regular", family: "'LXGW Marker Gothic',sans-serif",
        stack: "LXGW Marker Gothic", weights: [400],
        pkgs: [{ name: "@free-fonts/lxgw-marker-gothic", version: "1.0.0", css: "lxgw-marker-gothic.css" }] }
    ]
  },
  {
    id: "plangothic",
    nameEn: "Plangothic",
    nameZh: "遍黑體",
    displayText: "遍黑體",
    css: ["./plangothic/plangothic.css"],
    upstream: "https://github.com/Fitzgerald-Porthmouth-Koenigsegg/Plangothic_Project",
    license: "SIL OFL 1.1",
    variants: [
      { key: "default", label: "Regular", family: "'Plangothic',sans-serif", stack: "Plangothic", weights: [400],
        pkgs: [{ name: "@free-fonts/plangothic", version: "1.0.0", css: "plangothic.css" }] }
    ]
  },
  {
    id: "jigmo",
    nameEn: "Jigmo",
    nameZh: "字雲",
    displayText: "字雲",
    css: [
      "https://unpkg.com/@free-fonts/jigmo@1.0.0/jigmo.css",
      "https://unpkg.com/@free-fonts/jigmo-sc@1.0.0/jigmo-sc.css",
      "https://unpkg.com/@free-fonts/jigmo-tc@1.0.0/jigmo-tc.css"
    ],
    upstream: "https://kamichikoichi.github.io/jigmo/",
    license: "IPA Font License 1.0",
    autoByLang: { "zh-Hans": "sc", "zh-Hant": "tc", en: "base" },
    variants: [
      { key: "base", label: "Original", family: '"Jigmo",serif', stack: "Jigmo", weights: [400],
        pkgs: [{ name: "@free-fonts/jigmo", version: "1.0.0", css: "jigmo.css" }] },
      { key: "sc", label: "SC", family: '"Jigmo SC",serif', stack: "Jigmo SC", weights: [400],
        pkgs: [{ name: "@free-fonts/jigmo-sc", version: "1.0.0", css: "jigmo-sc.css" }] },
      { key: "tc", label: "TC", family: '"Jigmo TC",serif', stack: "Jigmo TC", weights: [400],
        pkgs: [{ name: "@free-fonts/jigmo-tc", version: "1.0.0", css: "jigmo-tc.css" }] }
    ]
  },
  {
    id: "noto-serif",
    nameEn: "Noto Serif CJK",
    nameZh: "思源宋體",
    shortEn: "Noto Serif",
    displayText: "思源宋體",
    css: [],
    upstream: "https://fonts.google.com/noto",
    license: "SIL OFL 1.1",
    autoByLang: { "zh-Hans": "sc", "zh-Hant": "tc", en: "sc" },
    variants: [
      { key: "sc", label: "SC", family: '"Noto Serif SC",serif', stack: "Noto Serif SC", weights: [400, 500, 600] },
      { key: "tc", label: "TC", family: '"Noto Serif TC",serif', stack: "Noto Serif TC", weights: [400, 500, 600] }
    ]
  },
  {
    id: "noto-sans",
    nameEn: "Noto Sans CJK",
    nameZh: "思源黑體",
    shortEn: "Noto Sans",
    displayText: "思源黑體",
    css: [],
    upstream: "https://fonts.google.com/noto",
    license: "SIL OFL 1.1",
    autoByLang: { "zh-Hans": "sc", "zh-Hant": "tc", en: "sc" },
    variants: [
      { key: "sc", label: "SC", family: '"Noto Sans SC",sans-serif', stack: "Noto Sans SC", weights: [400, 500] },
      { key: "tc", label: "TC", family: '"Noto Sans TC",sans-serif', stack: "Noto Sans TC", weights: [400, 500] }
    ]
  }
];

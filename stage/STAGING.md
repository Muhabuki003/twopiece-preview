# STAGING — The Two-Piece Edit

**Six-piece women's activewear capsule. Static HTML, staged on disk only.**

> **Status: LOCAL ONLY — nothing has been uploaded, published, deployed or written to Shopify or TeemDrop.**
> Every page is a plain `.html` file that opens directly from disk (`file://`). There is no build step
> required to view the site, no analytics, no cookies, no cart, no external requests of any kind.

- Location: `/root/stage/twopiece`
- Built: 2026-10-26
- Entry point: `/root/stage/twopiece/index.html`
- Source data: `spec.json` (TeemDrop SPU export, already fetched — not re-fetched for this build)
- Supplier copy: `assets/<slug>/detail.json` (used verbatim for the fact bullets)

---

## 1. View it

```bash
# straight from disk
xdg-open /root/stage/twopiece/index.html      # or open the file in any browser

# or over HTTP (127.0.0.1:8099 is occupied on this host by an unrelated dashboard
# process, so the documented port is bound on the 127.0.0.2 loopback alias instead)
python3 -m http.server 8099 --bind 127.0.0.2 --directory /root/stage/twopiece
# → http://127.0.0.2:8099/index.html
```

---

## 2. The six SKUs

| # | Page | Piece | SPU | Colourways | Sizes | Variants | Unit cost | Retail |
|---|------|-------|-----|-----------:|-------|---------:|----------:|-------:|
| 01 | `bra.html` | Faux Two-Piece Bra | SUWOCIB00672 | 5 | S · M · L · XL | 12 | $7.39 | $32.99 |
| 02 | `cami.html` | Halter Cami | SUSPAWY00629 | 6 | S · M · L · XL | 24 | $7.85 | $32.99 |
| 03 | `ls.html` | Halter Long Sleeve | SUSPAWY00468 | 16 (4 colours × 4 builds) | S · M · L · XL | 64 | $5.15 – $12.11 | $37.99 |
| 04 | `pants.html` | Wide-Leg Pants | SUSPAWY00650 | 5 | S · M · L · XL · XXL | 25 | $5.38 | $36.99 |
| 05 | `fold.html` | Fold-Over Wide-Leg Pants | SUSPAWY00645 | 12 | S · M · L · XL | 39 | $11.10 | $39.99 |
| 06 | `fauxset.html` | Faux Two-Piece Set | SUSPAWY00668 | 4 | S · M · L · XL | 9 | $17.96 | $64.99 |
| — | **capsule** | **6 pieces** | — | **48** | **S – XXL** | **173** | **$54.83** | **$245.94** |

Unit cost = TeemDrop wholesale, per piece, USD, before freight/duties. Retail = **proposed** price for this
capsule (bra 32.99, cami 32.99, ls 37.99, pants 36.99, fold 39.99, fauxset 64.99). Each product page shows
retail as the price with a small "unit cost $X" line beside it.

Sizes shown are the union across colourways. Availability per colourway is enforced on each page: size chips
that the selected colourway does not carry render greyed, dashed, `aria-disabled="true"` and carry the tooltip
_"not available in this colour"_.

---

## 3. Files (110)

### 3.1 Pages and shared assets (11)

| File | Bytes | Purpose |
|---|---:|---|
| `index.html` | 12,5 KB | Collection overview: 6 cards + spec sheet |
| `bra.html` | 9,3 KB | Faux Two-Piece Bra |
| `cami.html` | 8,8 KB | Halter Cami |
| `ls.html` | 12,7 KB | Halter Long Sleeve |
| `pants.html` | 8,8 KB | Wide-Leg Pants |
| `fold.html` | 10,9 KB | Fold-Over Wide-Leg Pants |
| `fauxset.html` | 8,9 KB | Faux Two-Piece Set |
| `assets/site.css` | 14,2 KB | Shared stylesheet (system font stack, light theme) |
| `assets/site.js` | 3,6 KB | Gallery swap, colourway + size availability (plain ES5, no fetch) |
| `spec.json` | 14,3 KB | Input spec (untouched) |
| `STAGING.md` | 21,4 KB | This manifest |

### 3.2 Derivative assets — created for this build (6)

The Wide-Leg Pants supplier frames carry large baked-in marketing type. Six text-free crops were cut locally
from those originals (PIL, no resampling beyond the hero, quality 88):

`assets/pants/crop/hero.jpg` (full-length off-white), `black.jpg`, `off-white.jpg`, `gray.jpg`, `brown.jpg`,
`mist-blue.jpg`.

### 3.3 Supplier assets — input, untouched (92)

| Directory | Files |
|---|---|
| `assets/bra/` | `0.jpg` `1.jpg` `2.jpg` `3.jpg` `4.jpg` `5.jpg` `detail.json` |
| `assets/bra/colours/` | `azure-blue-against-yellow.jpg` `blue-and-red-collide.jpg` `dark-blue-with-yellow-accents.jpg` `meteorite-black-against-yellow.jpg` `pomegranate-red-against-blue.jpg` |
| `assets/cami/` | `0.jpg` `1.jpg` `2.jpg` `3.jpg` `4.jpg` `5.jpg` `detail.json` |
| `assets/cami/colours/` | `black.jpg` `dark-brown.jpg` `green.jpg` `navy-blue.jpg` `purple.jpg` `white.jpg` |
| `assets/ls/` | `0.jpg` `1.jpg` `2.jpg` `3.jpg` `4.jpg` `5.jpg` `detail.json` |
| `assets/ls/colours/` | `advanced-black-long-sleeves-trousers.jpg` `badge-blue-bra.jpg` `badge-blue-long-sleeves-shorts.jpg` `badge-blue-long-sleeves-trousers.jpg` `badge-blue-long-sleeves.jpg` `extremely-gray-bra.jpg` `extremely-gray-long-sleeves-shorts.jpg` `extremely-gray-long-sleeves-trousers.jpg` `extremely-gray-long-sleeves.jpg` `high-end-black-long-sleeves-shorts.jpg` `premium-black-bra.jpg` `premium-black-long-sleeves.jpg` `swan-white-bra.jpg` `swan-white-long-sleeves-long-pants.jpg` `swan-white-long-sleeves-shorts.jpg` `swan-white-long-sleeves.jpg` |
| `assets/pants/` | `0.jpg` `1.jpg` `2.jpg` `3.jpg` `4.jpg` `5.jpg` `detail.json` |
| `assets/pants/colours/` | `black.jpg` `brown.jpg` `gray.jpg` `mist-blue.jpg` `off-white.jpg` |
| `assets/fold/` | `0.jpg` `1.jpg` `2.jpg` `3.jpg` `4.jpg` `5.jpg` `detail.json` |
| `assets/fold/colours/` | `badge-blue.jpg` `berry-rose.jpg` `black-coffee.jpg` `cream-apricot.jpg` `eggplant-purple.jpg` `falling-cherry-blossom-powder.jpg` `lilac-purple.jpg` `mist-charcoal-gray.jpg` `moss-green.jpg` `olive-green.jpg` `phantom-blue.jpg` `raspberry-red.jpg` |
| `assets/fauxset/` | `0.jpg` `1.jpg` `2.jpg` `3.jpg` `4.jpg` `5.jpg` `detail.json` |
| `assets/fauxset/colours/` | `biluo-blue-yellow.jpg` `maoqing-blue-red.jpg` `maoqing-blue-yellow.jpg` `pomegranate-red-blue.jpg` |

**Image files: 90 JPEGs** (84 supplier originals + 6 crops). Total staging directory: 110 files, ~28.8 MB.

### 3.4 Tooling (2, optional)

| File | Purpose |
|---|---|
| `tools/build_pages.py` | Generator used to write the 7 HTML files (provenance only — **not needed to view or edit the site**) |
| `tools/verify.py` | The verification harness — re-runnable, exits non-zero on any failure |
| `tools/verify-output.txt` | Saved output of the final verification run (reproduced in §5) |

---

## 4. Design and data decisions

**Look and feel** — one reference governs the whole build: a flat-lay of a burgundy/wine halter with
powder-blue fold-over wide-leg pants on a cream rug. Palette: wine `#5C1A2B`, powder blue `#8FA6CE`,
cream `#F3EEE6`, ink `#141110`. Light theme, near-black text, thin hairlines, small-caps labels,
tabular numerals, serif display over a system sans, generous white space, no shadows, no gradients on text,
no glassmorphism. Every card and bullet list carries the colour-block motif (wine / powder-blue alternation,
two-tone colourway swatches) rather than decoration.

**No text over photography.** No captions, badges, price tags or labels are overlaid on any image. Where a
supplier frame had baked-in marketing type, a different local frame was used or the frame was cropped before
use (see §4.1) — no remote substitutes were invented.

**Default selection.** Each page defaults to its first colourway (`bra` Azure blue / yellow, `cami` White,
`ls` Premium black — Long sleeve top, `pants` Black, `fold` Cream apricot, `fauxset` Pomegranate red / blue)
and the main image is that colourway's own photograph.

**Halter Long Sleeve structure.** The SPU carries 4 colours × 4 builds (long sleeve top, bra, + shorts,
+ trousers) = 16 selectable colourways, so the selector shows 16 chips labelled `Colour — Build`. All 16 are
S–XL, so nothing is greyed on that page.

### 4.1 Imagery notes

- `pants` — the five colourway frames and the six root frames all carry supplier typography
  ("skirt yoga pants", "FEELSOFT", a size chart). The page uses six locally cut, text-free crops
  (`assets/pants/crop/`) instead. The full-length shot is the off-white garment; the other five are
  waistband/leg detail crops, which reads as a colour study. **Production needs reshoots.**
- `ls` — root frame `5.jpg` has a vertical "COLOUR premium black" strip, so it is not used.
- `bra` — root frames `0.jpg`, `1.jpg`, `2.jpg` carry a supplier label / callouts / fabric copy and are not
  used; `3.jpg` (back), `4.jpg` (front), `5.jpg` (black) and the colourway shots are clean.
- `fold` — `3.jpg` is a fabric macro with copy; the page uses `0/1/2/4/5` and the clean colourway shots.
- `fauxset` — `0.jpg`/`1.jpg` have a small "Optional Color: 5 colors available" swatch block and `2.jpg`
  has inset callouts; the page leads with colourway shots and `3/4/5`.

### 4.2 Data discrepancy found (resolved toward the SPU)

The brief describes Fold-Over Wide-Leg Pants **Phantom blue** as "all S–XL". `spec.json` has it at
**M, L, XL**. Availability is driven from `spec.json` (the fetched SPU data), so the page greys out S for
Phantom blue. Flagged here rather than silently "fixed". (This also explains 39 variants, not 40.)

---

## 5. Verification — 2026-10-26

Harness: `tools/verify.py` → **83 checks, 83 passed, 0 failed**. Full output also saved to
`tools/verify-output.txt`.

```bash
python3 -m http.server 8099 --bind 127.0.0.2 --directory /root/stage/twopiece &
python3 tools/verify.py ; echo exit=$?      # exit=0
```

What it actually does: `curl` every page and every referenced path (and every other file in `assets/`),
decode every JPEG with PIL, parse every `<img src>`, and diff the inline `window.PRODUCT` data against
`spec.json`.

```text
==============================================================================
A. HTTP 200 — pages  (curl http://127.0.0.2:8099/)
==============================================================================
PASS  index.html                                                 HTTP 200
PASS  bra.html                                                   HTTP 200
PASS  cami.html                                                  HTTP 200
PASS  ls.html                                                    HTTP 200
PASS  pants.html                                                 HTTP 200
PASS  fold.html                                                  HTTP 200
PASS  fauxset.html                                               HTTP 200

==============================================================================
B. HTTP 200 — every referenced local asset  (38 unique)
==============================================================================
PASS  assets/bra/3.jpg                                           HTTP 200
PASS  assets/bra/4.jpg                                           HTTP 200
PASS  assets/bra/5.jpg                                           HTTP 200
PASS  assets/bra/colours/azure-blue-against-yellow.jpg           HTTP 200
PASS  assets/bra/colours/meteorite-black-against-yellow.jpg      HTTP 200
PASS  assets/bra/colours/pomegranate-red-against-blue.jpg        HTTP 200
PASS  assets/cami/0.jpg                                          HTTP 200
PASS  assets/cami/1.jpg                                          HTTP 200
PASS  assets/cami/2.jpg                                          HTTP 200
PASS  assets/cami/3.jpg                                          HTTP 200
PASS  assets/cami/4.jpg                                          HTTP 200
PASS  assets/cami/colours/white.jpg                              HTTP 200
PASS  assets/fauxset/0.jpg                                       HTTP 200
PASS  assets/fauxset/3.jpg                                       HTTP 200
PASS  assets/fauxset/4.jpg                                       HTTP 200
PASS  assets/fauxset/5.jpg                                       HTTP 200
PASS  assets/fauxset/colours/biluo-blue-yellow.jpg               HTTP 200
PASS  assets/fauxset/colours/pomegranate-red-blue.jpg            HTTP 200
PASS  assets/fold/0.jpg                                          HTTP 200
PASS  assets/fold/1.jpg                                          HTTP 200
PASS  assets/fold/2.jpg                                          HTTP 200
PASS  assets/fold/4.jpg                                          HTTP 200
PASS  assets/fold/5.jpg                                          HTTP 200
PASS  assets/fold/colours/cream-apricot.jpg                      HTTP 200
PASS  assets/ls/0.jpg                                            HTTP 200
PASS  assets/ls/1.jpg                                            HTTP 200
PASS  assets/ls/2.jpg                                            HTTP 200
PASS  assets/ls/3.jpg                                            HTTP 200
PASS  assets/ls/4.jpg                                            HTTP 200
PASS  assets/ls/colours/premium-black-long-sleeves.jpg           HTTP 200
PASS  assets/pants/crop/black.jpg                                HTTP 200
PASS  assets/pants/crop/brown.jpg                                HTTP 200
PASS  assets/pants/crop/gray.jpg                                 HTTP 200
PASS  assets/pants/crop/hero.jpg                                 HTTP 200
PASS  assets/pants/crop/mist-blue.jpg                            HTTP 200
PASS  assets/pants/crop/off-white.jpg                            HTTP 200
PASS  assets/site.css                                            HTTP 200
PASS  assets/site.js                                             HTTP 200

==============================================================================
B2. HTTP 200 — every file under assets/ (referenced or not) + spec.json
==============================================================================
PASS  all 99 files on disk serve HTTP 200                        []

==============================================================================
B3. Every JPEG on disk decodes (PIL) with sane dimensions
==============================================================================
PASS  90 JPEGs decode                                            []
PASS  90 JPEGs are >= 300px on both sides                        []

==============================================================================
C. Every <img src> resolves to a file on disk
==============================================================================
PASS  index.html — 7 <img> tags                                  all present
PASS  bra.html — 10 <img> tags                                   all present
PASS  cami.html — 10 <img> tags                                  all present
PASS  ls.html — 10 <img> tags                                    all present
PASS  pants.html — 10 <img> tags                                 all present
PASS  fold.html — 10 <img> tags                                  all present
PASS  fauxset.html — 10 <img> tags                               all present

==============================================================================
D. Each product page references >= 3 existing images
==============================================================================
PASS  bra.html — 9 distinct existing images                      
PASS  cami.html — 9 distinct existing images                     
PASS  ls.html — 9 distinct existing images                       
PASS  pants.html — 9 distinct existing images                    
PASS  fold.html — 9 distinct existing images                     
PASS  fauxset.html — 9 distinct existing images                  

==============================================================================
E. Excluded 7th SKU absent (keyword scan of every text file)
==============================================================================
PASS  excluded-SKU keywords absent from pages, CSS and JS        0 matches across 9 text files

==============================================================================
F. No external references (no CDN, no Google Fonts, no remote images)
==============================================================================
PASS  no http(s)/CDN/font references                             []

==============================================================================
G. Mobile CSS — no fixed width / min-width above 390px
==============================================================================
PASS  site.css width/min-width > 390px                           7 fixed widths declared, max 54 px
      note: 4 max-width caps (420, 520, 719, 1180 px) — caps, not fixed widths
PASS  inline widths > 390px in pages                             []
PASS  tap targets: chips declared min-height:44px                
PASS  tap targets: thumbnails declared min-height:44px           
PASS  thumbnail grid reflows at 420px                            

==============================================================================
H. Page furniture (viewport, title, staging notice, noindex)
==============================================================================
PASS  index.html furniture                                       complete
PASS  bra.html furniture                                         complete
PASS  cami.html furniture                                        complete
PASS  ls.html furniture                                          complete
PASS  pants.html furniture                                       complete
PASS  fold.html furniture                                        complete
PASS  fauxset.html furniture                                     complete

==============================================================================
I. Data integrity — inline PRODUCT objects vs spec.json
==============================================================================
PASS  bra — SPU SUWOCIB00672, 5 colourways, 12 variants          
PASS  cami — SPU SUSPAWY00629, 6 colourways, 24 variants         
PASS  ls — SPU SUSPAWY00468, 16 colourways, 64 variants          
PASS  pants — SPU SUSPAWY00650, 5 colourways, 25 variants        
PASS  fold — SPU SUSPAWY00645, 12 colourways, 39 variants        
PASS  fauxset — SPU SUSPAWY00668, 4 colourways, 9 variants       

==============================================================================
J. Cross-linking (index <-> products)
==============================================================================
PASS  index links to all six product pages                       []
PASS  every product page links back to index                     []

==============================================================================
SUMMARY
==============================================================================
checks: 83   passed: 83   failed: 0   <img> tags across pages: 67   assets referenced: 38
ALL CHECKS PASSED
```

### 5.1 Headless browser checks (`file://`, Chromium via CDP)

| Check | Result |
|---|---|
| All 7 pages open from `file://` (no server) | **PASS** — 7/7 rendered; interactions below all work, so no script error blocked init |
| `document.documentElement.scrollWidth` at 390 × 844 viewport | **PASS** — 390 on all 7 pages (no horizontal scroll) |
| Elements extending past the 390px viewport | **PASS** — none on the 6 product pages; index only the visually-hidden `<th>` inside the clipped `<thead>` (no overflow: `scrollWidth` stays 390) |
| Gallery thumbnail click swaps main image | **PASS** — all 6 pages, 6 thumbs each, `#mainImg` src follows the thumb and the active state moves |
| Script boots (size chips are built by JS, so a throw would leave the group empty) | **PASS** — every page renders its size chips and its colour chips: 5, 6, 16, 5, 12, 4 |
| Default colourway selection | **PASS** — 0 disabled sizes on 5 pages; `fauxset` default (Pomegranate red / blue, S–M–L) correctly greys XL |
| Colourway chip swaps to that colourway's photo | **PASS** — `bra` → `assets/bra/colours/meteorite-black-against-yellow.jpg`, `fold` → `assets/fold/colours/lilac-purple.jpg`, `pants` → `assets/pants/crop/black.jpg` |
| Partial availability disables sizes + tooltip | **PASS** — `fold` Lilac purple: S enabled, M/L/XL `aria-disabled="true"` with `title="not available in this colour"`; `bra` Meteorite black: XL only |
| Clicking a disabled size does nothing | **PASS** — selection line stays "… · select a size" |
| Selecting an available size | **PASS** — reads "Meteorite black / yellow · Size XL" |
| Tap targets ≥ 40px | **PASS** — chips `min-height:44px`, thumbnails `min-height:44px` |
| Staging notice present on every page | **PASS** — banner + in-panel notice + footer on all 7 |

### 5.2 Not verified (out of scope for local staging)

- No real-device testing (iOS Safari / Android Chrome), only emulated 390px in Chromium.
- No Lighthouse/Core Web Vitals run; images are full-size supplier files (~29 MB total) and would need
  resizing + CDN delivery before a real storefront launch.
- No checkout, inventory, shipping-rate or tax logic exists to test — none was requested.
- Colour rendering is as-shot; the wine/powder-blue palette is styling, not a guarantee that a garment's
  physical colour matches its swatch.

---

## 6. Before this can go live

1. Reshoot or relicense imagery — several supplier frames are marketing graphics, not editorial photography.
2. Optimise images (WebP/AVIF, responsive `srcset`); 29 MB will not ship as-is.
3. Confirm the Phantom blue size run with the supplier (M–XL vs S–XL).
4. Approve retail prices; add size chart, fabric care, shipping and returns copy.
5. Replace `robots: noindex` and the staging banners, then move to a real host — none of which is done here.

---

## 7. Confirmations

- **No uploads, deploys, DNS changes, or Shopify/TeemDrop API writes were made.** No credentials were read.
- No API calls were made during this build; all data and images came from the local `spec.json` and
  `assets/`.
- No remote URLs appear in any page, stylesheet or script (asserted by check F, 0 matches).
- The excluded seventh SKU is **not built, not linked and not referenced** anywhere in the site; check E
  greps all 9 text files for the excluded variant's keywords and returns 0 matches.

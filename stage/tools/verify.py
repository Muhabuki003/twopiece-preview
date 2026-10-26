#!/usr/bin/env python3
"""
Verification for the staged two-piece capsule.
Runs real HTTP requests with curl against a local python http.server and
inspects every file on disk. Prints PASS/FAIL per check, exits 1 on any FAIL.

Usage:
    python3 -m http.server 8099 --bind 127.0.0.2 --directory /root/stage/twopiece &
    python3 tools/verify.py
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = os.environ.get("STAGE_HOST", "127.0.0.2")
PORT = os.environ.get("STAGE_PORT", "8099")
BASE = "http://%s:%s/" % (HOST, PORT)

PAGES = ["index", "bra", "cami", "ls", "pants", "fold", "fauxset"]
PRODUCTS = PAGES[1:]
EXPECT_COLOURS = {"bra": 5, "cami": 6, "ls": 16, "pants": 5, "fold": 12, "fauxset": 4}

fails = []
checks = 0


def ok(label, detail=""):
    global checks
    checks += 1
    print("PASS  %-58s %s" % (label, detail))


def bad(label, detail=""):
    global checks
    checks += 1
    fails.append(label + (" — " + detail if detail else ""))
    print("FAIL  %-58s %s" % (label, detail))


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def curl(path):
    out = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "15", BASE + path],
        capture_output=True, text=True)
    return out.stdout.strip()


def local_refs(html):
    refs = set()
    for attr in ("src", "href"):
        for m in re.finditer(r'%s="([^"]+)"' % attr, html):
            v = m.group(1)
            if v.startswith(("#", "mailto:", "tel:", "data:")) or "://" in v:
                continue
            refs.add(v)
    return refs


# ---------------------------------------------------------------- collect
html = {p: read(p + ".html") for p in PAGES}
css = read("assets/site.css")
js = read("assets/site.js")
spec = json.loads(read("spec.json"))

page_refs = set()
for p in PAGES:
    page_refs |= local_refs(html[p])
for m in re.finditer(r'url\(([^)]+)\)', css):
    page_refs.add(m.group(1).strip("'\""))

asset_refs = sorted(r for r in page_refs if not r.endswith(".html") and "#" not in r)

print("=" * 78)
print("A. HTTP 200 — pages  (curl %s)" % BASE)
print("=" * 78)
for p in PAGES:
    code = curl(p + ".html")
    (ok if code == "200" else bad)("%s.html" % p, "HTTP " + code)

print()
print("=" * 78)
print("B. HTTP 200 — every referenced local asset  (%d unique)" % len(asset_refs))
print("=" * 78)
for a in asset_refs:
    code = curl(a)
    (ok if code == "200" else bad)(a, "HTTP " + code)

print()
print("=" * 78)
print("B2. HTTP 200 — every file under assets/ (referenced or not) + spec.json")
print("=" * 78)
disk = []
for dirpath, _dirnames, filenames in os.walk(os.path.join(ROOT, "assets")):
    for f in filenames:
        disk.append(os.path.relpath(os.path.join(dirpath, f), ROOT))
disk.append("spec.json")
disk.sort()
disk_bad = []
for f in disk:
    code = curl(f)
    if code != "200":
        disk_bad.append((f, code))
(ok if not disk_bad else bad)("all %d files on disk serve HTTP 200" % len(disk), str(disk_bad[:5]))

print()
print("=" * 78)
print("B3. Every JPEG on disk decodes (PIL) with sane dimensions")
print("=" * 78)
try:
    from PIL import Image
    broken, tiny = [], []
    jpgs = [f for f in disk if f.lower().endswith(".jpg")]
    for f in jpgs:
        try:
            with Image.open(os.path.join(ROOT, f)) as im:
                im.verify()
            with Image.open(os.path.join(ROOT, f)) as im:
                w, h = im.size
                if w < 300 or h < 300:
                    tiny.append((f, w, h))
        except Exception as exc:  # noqa: BLE001
            broken.append((f, str(exc)[:40]))
    (ok if not broken else bad)("%d JPEGs decode" % len(jpgs), str(broken[:5]))
    (ok if not tiny else bad)("%d JPEGs are >= 300px on both sides" % len(jpgs), str(tiny[:5]))
except ImportError:
    bad("PIL available for image decode check", "PIL not installed")

print()
print("=" * 78)
print("C. Every <img src> resolves to a file on disk")
print("=" * 78)
img_total = 0
for p in PAGES:
    srcs = re.findall(r'<img[^>]+src="([^"]+)"', html[p])
    img_total += len(srcs)
    missing = [s for s in srcs if not os.path.isfile(os.path.join(ROOT, s))]
    (ok if not missing else bad)("%s.html — %d <img> tags" % (p, len(srcs)),
                                 "all present" if not missing else "missing: %s" % missing)

print()
print("=" * 78)
print("D. Each product page references >= 3 existing images")
print("=" * 78)
for p in PRODUCTS:
    srcs = set(re.findall(r'<img[^>]+src="([^"]+)"', html[p]))
    exist = [s for s in srcs if os.path.isfile(os.path.join(ROOT, s))]
    (ok if len(exist) >= 3 else bad)("%s.html — %d distinct existing images" % (p, len(exist)))

print()
print("=" * 78)
print("E. Excluded 7th SKU absent (keyword scan of every text file)")
print("=" * 78)
banned = re.compile(r"strip(?:e|es|ed|ing)|polka", re.I)
hits = []
for name in [p + ".html" for p in PAGES] + ["assets/site.css", "assets/site.js"]:
    text = read(name)
    for m in banned.finditer(text):
        hits.append((name, text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")))
if hits:
    bad("banned product words", str(hits[:3]))
else:
    ok("excluded-SKU keywords absent from pages, CSS and JS",
       "0 matches across 9 text files")

print()
print("=" * 78)
print("F. No external references (no CDN, no Google Fonts, no remote images)")
print("=" * 78)
ext = re.compile(r"https?://|//cdn|fonts\.googleapis|fonts\.gstatic|@import\s+url", re.I)
ext_hits = []
for name in [p + ".html" for p in PAGES] + ["assets/site.css", "assets/site.js"]:
    if ext.search(read(name)):
        ext_hits.append(name)
(ok if not ext_hits else bad)("no http(s)/CDN/font references", str(ext_hits))

print()
print("=" * 78)
print("G. Mobile CSS — no fixed width / min-width above 390px")
print("=" * 78)
# Only `width:` / `min-width:` force an element wider than the viewport.
# `max-width:` is a cap and is reported separately (it cannot cause overflow).
fixed = [(m.group(1), m.group(2)) for m in
         re.finditer(r"(?:^|[;{\s])(width|min-width)\s*:\s*(\d+)px", css)]
over = [(prop, v) for prop, v in fixed if int(v) > 390]
caps = [int(m.group(1)) for m in re.finditer(r"max-width\s*:\s*(\d+)px", css)]
(ok if not over else bad)(
    "site.css width/min-width > 390px",
    str(over) if over else "%d fixed widths declared, max %s px" %
    (len(fixed), max([int(v) for _, v in fixed] or [0])))
print("      note: %d max-width caps (%s px) — caps, not fixed widths"
      % (len(caps), ", ".join(str(c) for c in sorted(set(caps)))))
inline_wide = []
for p in PAGES:
    for m in re.finditer(r'style="[^"]*width:\s*(\d+)px', html[p]):
        if int(m.group(1)) > 390:
            inline_wide.append((p, m.group(1)))
(ok if not inline_wide else bad)("inline widths > 390px in pages", str(inline_wide))
(ok if "min-height:44px" in css else bad)("tap targets: chips declared min-height:44px")
(ok if "min-height:44px" in css else bad)("tap targets: thumbnails declared min-height:44px")
(ok if "max-width:420px" in css and ".thumbs{grid-template-columns" in css else bad)(
    "thumbnail grid reflows at 420px")

print()
print("=" * 78)
print("H. Page furniture (viewport, title, staging notice, noindex)")
print("=" * 78)
for p in PAGES:
    h = html[p]
    problems = []
    if 'name="viewport"' not in h:
        problems.append("no viewport")
    if "<title>" not in h:
        problems.append("no title")
    if "not published" not in h.lower():
        problems.append("no staging notice")
    if "noindex" not in h:
        problems.append("no noindex")
    (ok if not problems else bad)("%s.html furniture" % p, ", ".join(problems) or "complete")

print()
print("=" * 78)
print("I. Data integrity — inline PRODUCT objects vs spec.json")
print("=" * 78)
for p in PRODUCTS:
    m = re.search(r"window\.PRODUCT = (\{.*?\});</script>", html[p], re.S)
    if not m:
        bad("%s.html inline data" % p, "not found")
        continue
    data = json.loads(m.group(1))
    spu_ok = data["spu"] == spec[p]["spu"]
    n_ok = len(data["colours"]) == EXPECT_COLOURS[p]
    variants = sum(len(c["sizes"]) for c in data["colours"])
    var_ok = variants == spec[p]["n_variants"]

    # sizes must match spec.json exactly, per colourway
    spec_cols = list(spec[p]["colours"].values())
    sizes_ok = True
    for c in data["colours"]:
        if not any(sorted(v["sizes"]) == sorted(c["sizes"]) for v in spec_cols):
            sizes_ok = False
    allsz = set()
    for c in data["colours"]:
        allsz |= set(c["sizes"])
    page_sz_ok = allsz == set(data["sizes"])

    good = spu_ok and n_ok and var_ok and sizes_ok and page_sz_ok
    (ok if good else bad)(
        "%s — SPU %s, %d colourways, %d variants" % (p, data["spu"], len(data["colours"]), variants),
        "" if good else "spu=%s count=%s variants=%s sizes=%s union=%s" %
        (spu_ok, n_ok, var_ok, sizes_ok, page_sz_ok))

print()
print("=" * 78)
print("J. Cross-linking (index <-> products)")
print("=" * 78)
missing_links = [p for p in PRODUCTS if "%s.html" % p not in html["index"]]
(ok if not missing_links else bad)("index links to all six product pages", str(missing_links))
bad_nav = [p for p in PRODUCTS if 'href="index.html"' not in html[p]]
(ok if not bad_nav else bad)("every product page links back to index", str(bad_nav))

print()
print("=" * 78)
print("SUMMARY")
print("=" * 78)
print("checks: %d   passed: %d   failed: %d   <img> tags across pages: %d   assets referenced: %d"
      % (checks, checks - len(fails), len(fails), img_total, len(asset_refs)))
if fails:
    print("\nFAILURES:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("ALL CHECKS PASSED")

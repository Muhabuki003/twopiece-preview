#!/usr/bin/env python3
"""
Build the six staged product pages + collection index for "The Two-Piece Edit".

This script is OPTIONAL provenance only. The generated .html files are already
committed into /root/stage/twopiece and are fully static: no build step is
required to view them (open index.html from disk).

Source of truth: ./spec.json (TeemDrop SPU data, already fetched) and
./assets/<slug>/detail.json (supplier copy used verbatim for the fact bullets).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = json.load(open(os.path.join(ROOT, "spec.json")))

RETAIL = {"bra": 32.99, "cami": 32.99, "ls": 37.99,
          "pants": 36.99, "fold": 39.99, "fauxset": 64.99}

ORDER = ["bra", "cami", "ls", "pants", "fold", "fauxset"]

# ---------------------------------------------------------------- colourways
# spec colour key -> (display name, swatch pair)
COLOURS = {
    "bra": [
        ("Azure blue against yellow", "Azure blue / yellow", "#9FD0DC", "#F2E3B0", ["S", "M", "L", "XL"]),
        ("Pomegranate red against blue", "Pomegranate red / blue", "#8E2B3F", "#A6D5E2", ["S", "M", "L"]),
        ("Blue and red collide", "Blue / red", "#52739B", "#A63A4E", ["L", "XL"]),
        ("Dark blue with yellow accents", "Dark blue / yellow", "#3C5878", "#F2E3B0", ["S", "XL"]),
        ("Meteorite black against yellow", "Meteorite black / yellow", "#26262A", "#F2E3B0", ["XL"]),
    ],
    "cami": [
        ("White", "White", "#F7F4EE", None, ["S", "M", "L", "XL"]),
        ("Dark brown", "Dark brown", "#4A3A31", None, ["S", "M", "L", "XL"]),
        ("Green", "Green", "#5F7A50", None, ["S", "M", "L", "XL"]),
        ("Navy blue", "Navy blue", "#2B3A54", None, ["S", "M", "L", "XL"]),
        ("Purple", "Purple", "#6E5A86", None, ["S", "M", "L", "XL"]),
        ("Black", "Black", "#1F1E1E", None, ["S", "M", "L", "XL"]),
    ],
    "pants": [
        ("Black", "Black", "#1C1C1E", None, ["S", "M", "L", "XL", "XXL"]),
        ("Off-white", "Off-white", "#EFE8DA", None, ["S", "M", "L", "XL", "XXL"]),
        ("Gray", "Gray", "#A9A9A7", None, ["S", "M", "L", "XL", "XXL"]),
        ("Brown", "Brown", "#6B5748", None, ["S", "M", "L", "XL", "XXL"]),
        ("Mist blue", "Mist blue", "#9BB3CE", None, ["S", "M", "L", "XL", "XXL"]),
    ],
    "fold": [
        ("Cream apricot", "Cream apricot", "#F0E3C9", None, ["S", "M", "L", "XL"]),
        ("Mist charcoal gray", "Mist charcoal", "#4C4E52", None, ["S", "M", "L", "XL"]),
        ("Olive green", "Olive green", "#5C6242", None, ["S", "M", "L", "XL"]),
        ("Berry rose", "Berry rose", "#B23A63", None, ["S", "M", "L", "XL"]),
        ("Black coffee", "Black coffee", "#4A3B33", None, ["S", "M", "L", "XL"]),
        ("Badge blue", "Badge blue", "#4E6B8C", None, ["S", "M", "L", "XL"]),
        ("Moss green", "Moss green", "#A8B08A", None, ["S", "M", "L", "XL"]),
        ("Phantom blue", "Phantom blue", "#C3D4EA", None, ["M", "L", "XL"]),
        ("Raspberry red", "Raspberry red", "#A61E45", None, ["M", "L", "XL"]),
        ("Eggplant purple", "Eggplant purple", "#6B5A72", None, ["S", "XL"]),
        ("Falling cherry blossom powder", "Cherry blossom", "#F2C6CF", None, ["M", "L"]),
        ("Lilac purple", "Lilac purple", "#B7A3CE", None, ["S"]),
    ],
    "fauxset": [
        ("Pomegranate Red Blue", "Pomegranate red / blue", "#8E2B3F", "#33465E", ["S", "M", "L"]),
        ("Biluo Blue Yellow", "Biluo blue / yellow", "#A6D5E2", "#F2E3B4", ["S", "M", "XL"]),
        ("Maoqing Blue Yellow", "Maoqing blue / yellow", "#33465E", "#F2E3B4", ["S", "XL"]),
        ("Maoqing Blue Red", "Maoqing blue / red", "#33465E", "#8E2B3F", ["XL"]),
    ],
}

LS_COLOUR = {"Premium black": "#1E1E20", "Heather grey": "#B9B7B4",
             "Swan white": "#F6F4EF", "Badge blue": "#4E6B8C"}

# Long-sleeve: 4 colours x 4 builds, expanded from the 16 spec colour keys.
def ls_colours():
    spec_keys = SPEC["ls"]["colours"]
    bases = [("Premium black", "Premium black"), ("Heather grey", "Heather grey"),
             ("Swan white", "Swan white"), ("Badge blue", "Badge blue")]
    builds = ["Long sleeve top", "Bra", "+ Shorts", "+ Trousers"]

    def colour_of(k):
        if "badge blue" in k:
            return "Badge blue"
        if "white" in k:
            return "Swan white"
        if "gray" in k or "grey" in k:
            return "Heather grey"
        if "black" in k:
            return "Premium black"
        return None

    def build_of(k):
        if "shorts" in k:
            return "+ Shorts"
        if "trousers" in k or "long pants" in k:
            return "+ Trousers"
        if k.rstrip().endswith("bra"):
            return "Bra"
        return "Long sleeve top"

    table = {}
    for key, val in spec_keys.items():
        k = key.lower()
        table[(colour_of(k), build_of(k))] = (key, val)

    out = []
    for label, _ in bases:
        for blabel in builds:
            hit = table.get((label, blabel))
            assert hit, ("ls combination missing", label, blabel)
            key, val = hit
            out.append((key, "%s — %s" % (label, blabel),
                        LS_COLOUR[label], None, val["sizes"], val.get("img")))
    return out


# ---------------------------------------------------------------- images
IMAGES = {
    "bra": [
        ("assets/bra/colours/azure-blue-against-yellow.jpg", "Faux Two-Piece Bra in azure blue with yellow lining"),
        ("assets/bra/4.jpg", "Faux two-piece bra, front view, pomegranate red"),
        ("assets/bra/3.jpg", "Hollow square back with fixed double straps"),
        ("assets/bra/5.jpg", "Meteorite black bra with cream halter lining"),
        ("assets/bra/colours/pomegranate-red-against-blue.jpg", "Pomegranate red against powder blue"),
        ("assets/bra/colours/meteorite-black-against-yellow.jpg", "Meteorite black against yellow"),
    ],
    "cami": [
        ("assets/cami/colours/white.jpg", "Halter Cami in white, front view"),
        ("assets/cami/0.jpg", "Halter Cami in navy blue, styled with shorts"),
        ("assets/cami/1.jpg", "Backless halter neckline, navy blue"),
        ("assets/cami/2.jpg", "Halter Cami in black"),
        ("assets/cami/3.jpg", "Halter Cami in white, close crop"),
        ("assets/cami/4.jpg", "Halter Cami in dark brown"),
    ],
    "ls": [
        ("assets/ls/colours/premium-black-long-sleeves.jpg", "Halter Long Sleeve in premium black"),
        ("assets/ls/0.jpg", "Halter Long Sleeve in swan white with shorts"),
        ("assets/ls/1.jpg", "Long sleeve crop, side view, swan white"),
        ("assets/ls/2.jpg", "Back view of the long sleeve top and shorts"),
        ("assets/ls/3.jpg", "Halter Long Sleeve in premium black with shorts"),
        ("assets/ls/4.jpg", "Premium black long sleeve, front view"),
    ],
    "pants": [
        ("assets/pants/crop/black.jpg", "Black wide-leg pants, waist and skirt-overlay detail"),
        ("assets/pants/crop/hero.jpg", "Wide-Leg Pants in off-white, full length"),
        ("assets/pants/crop/off-white.jpg", "Off-white waistband and flared leg detail"),
        ("assets/pants/crop/gray.jpg", "Gray wide-leg pants, waist detail"),
        ("assets/pants/crop/brown.jpg", "Brown wide-leg pants, waist detail"),
        ("assets/pants/crop/mist-blue.jpg", "Mist blue wide-leg pants, waist detail"),
    ],
    "fold": [
        ("assets/fold/colours/cream-apricot.jpg", "Fold-Over Wide-Leg Pants in cream apricot"),
        ("assets/fold/0.jpg", "Fold-over waistband, olive green, front view"),
        ("assets/fold/1.jpg", "Olive green wide leg, three-quarter view"),
        ("assets/fold/2.jpg", "Olive green, side seam and drape"),
        ("assets/fold/4.jpg", "Olive green full length with fold-over waist"),
        ("assets/fold/5.jpg", "Cream apricot full length"),
    ],
    "fauxset": [
        ("assets/fauxset/colours/pomegranate-red-blue.jpg", "Faux Two-Piece Set in pomegranate red with blue pant"),
        ("assets/fauxset/3.jpg", "Set in navy with cream contrast waistband"),
        ("assets/fauxset/4.jpg", "Set in navy with cream waistband, front view"),
        ("assets/fauxset/5.jpg", "Set in navy with pomegranate waistband"),
        ("assets/fauxset/colours/biluo-blue-yellow.jpg", "Biluo blue with yellow waistband"),
        ("assets/fauxset/0.jpg", "Set in navy and pomegranate, studio view"),
    ],
}

# ---------------------------------------------------------------- copy
BULLETS = {
    "bra": [
        "Brushed 78% nylon / 22% spandex with a soft, skin-friendly hand.",
        "Colour-blocked panels over a faux two-piece cut — one garment, layered look.",
        "Fixed double shoulder straps and a halter neckline for support through full range.",
        "Full cup with a medium mould cup and chest pad; no underwire. Low-intensity support.",
    ],
    "cami": [
        "Seamless knit with four-way stretch and moisture-wicking yarn.",
        "Halter neckline with a backless cut and waist-high length.",
        "Built-in bra with a removable chest pad; regular fit, pullover entry.",
        "75% nylon / 25% spandex. Sized S/4 through XL/10.",
    ],
    "ls": [
        "Halterneck, long sleeve, cut tight to the body with a waist-length crop.",
        "78% nylon / 22% spandex with a textured threaded hand.",
        "Moisture-wicking; built for yoga, pilates and gym sessions.",
        "Offered four ways: long sleeve top, bra, or top with shorts or trousers.",
    ],
    "pants": [
        "High-rise waistband with gentle tummy-control compression.",
        "Polyester-spandex blend, high elasticity, thin hand.",
        "Slightly flared 7/8 leg with a wrap skirt overlay at the hip and tie detail.",
        "Invisible side pockets; butt-lift seam placement.",
        "The only piece in the capsule cut to XXL.",
    ],
    "fold": [
        "Brushed 78% nylon / 22% spandex, moisture-wicking.",
        "Fold-over waistband sits low-rise and adjusts the rise.",
        "Wide leg with a long, straight drape and a slimming line.",
        "Twelve colourways, four of them in partial size runs.",
        "Sizes S–XL; 1–4 cm measurement tolerance on the supplier spec.",
    ],
    "fauxset": [
        "Two pieces per set: bra top and wide-leg pant.",
        "Contrast colour-block waistband across the hip — the capsule motif.",
        "78% nylon / 22% spandex with a brushed nylon-spandex lining, quick-dry.",
        "High-rise with tummy control; chest pad included in the top.",
        "Nine colour/size combinations across four colourways.",
    ],
}

# Collection-grid image can differ from the gallery lead (pants leads with its
# default colourway, but the grid wants the full-length silhouette).
CARD_IMG = {"pants": ("assets/pants/crop/hero.jpg",
                      "Wide-Leg Pants in off-white, full length")}

DESC = {
    "bra": "A brushed sports bra built on the illusion of two layers: a powder-blue halter set inside a wine shell, held by fixed double straps.",
    "cami": "A seamless halter cami with a backless cut and a built-in shelf bra. The quiet half of the capsule.",
    "ls": "A halterneck long sleeve, cut close, sold as a top or as a two-piece with shorts or trousers.",
    "pants": "A high-rise, slightly flared 7/8 pant with a wrap skirt overlay at the hip and tie detail. The only XXL in the capsule.",
    "fold": "The reference piece: a low-rise fold-over waistband over a wide, straight leg. Twelve colourways, most in full size runs.",
    "fauxset": "Bra and wide-leg pant sold together, joined by a contrast waistband that reads as two pieces and behaves as one.",
}

SPECS = {
    "bra": [("Material", "78% nylon / 22% spandex"), ("Support", "Low intensity · full cup · no underwire"),
            ("Weight", "128 g"), ("Category", "Intimates · bras")],
    "cami": [("Material", "75% nylon / 25% spandex"), ("Fit", "Regular · waist-high · pullover"),
             ("Weight", "170 g"), ("Category", "Yoga tops")],
    "ls": [("Material", "78% nylon / 22% spandex"), ("Fit", "Tight · waist-length crop"),
           ("Weight", "280–380 g"), ("Category", "Yoga suits")],
    "pants": [("Material", "Polyester / spandex blend"), ("Length", "7/8 cropped · slightly flared"),
              ("Weight", "235 g"), ("Category", "Yoga pants")],
    "fold": [("Material", "78% nylon / 22% spandex"), ("Rise", "Low-rise · fold-over waistband"),
             ("Weight", "336 g"), ("Category", "Wide-leg pants")],
    "fauxset": [("Material", "78% nylon / 22% spandex"), ("Set includes", "Bra + wide-leg pant"),
                ("Weight", "460 g"), ("Category", "Yoga sets")],
}


def cost_str(slug):
    """Unit cost as displayed: '$7.39', or '$5.15 – $12.11' for ranged SKUs."""
    c = SPEC[slug]["price_range"]
    if "-" in c:
        lo, hi = c.split("-")
        return "$%.2f – $%.2f" % (float(lo), float(hi))
    return "$%.2f" % float(c)


# Pants: the supplier frames carry marketing type, so the page uses the
# locally cropped, text-free derivatives in assets/pants/crop/ instead.
IMG_OVERRIDE = {
    "pants": {
        "Black": "assets/pants/crop/black.jpg",
        "Off-white": "assets/pants/crop/off-white.jpg",
        "Gray": "assets/pants/crop/gray.jpg",
        "Brown": "assets/pants/crop/brown.jpg",
        "Mist blue": "assets/pants/crop/mist-blue.jpg",
    }
}


def colours_for(slug):
    if slug == "ls":
        return ls_colours()
    spec_cols = SPEC[slug]["colours"]
    over = IMG_OVERRIDE.get(slug, {})
    out = []
    for key, label, c1, c2, sizes in COLOURS[slug]:
        entry = spec_cols.get(key)
        assert entry, (slug, key)
        # availability comes from spec.json, never from the brief
        assert sorted(entry["sizes"]) == sorted(sizes), (slug, key, entry["sizes"], sizes)
        out.append((key, label, c1, c2, entry["sizes"], over.get(key, entry.get("img"))))
    return out


def swatch_html(c1, c2, cls="sw"):
    if c2:
        return ('<span class="%s" style="background:linear-gradient(90deg,%s 0 50%%,%s 50%% 100%%)" '
                'aria-hidden="true"></span>' % (cls, c1, c2))
    return '<span class="%s" style="background:%s" aria-hidden="true"></span>' % (cls, c1)


def head(title, desc):
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex,nofollow">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>""" % (title, desc)


BAR = """<div class="staging-bar"><div class="wrap"><strong>Staging preview — not published</strong><span>Local file build <span class="dot">/</span> no checkout <span class="dot">/</span> internal review</span></div></div>"""

HEADER = """<header class="site-head"><div class="wrap">
  <a class="wordmark" href="index.html">Two-Piece Edit</a>
  <nav class="site-nav" aria-label="Collection">
    <a href="index.html">All six pieces</a>
    <a href="index.html#specs">Spec sheet</a>
  </nav>
</div></header>"""

FOOTER = """<footer class="site-foot"><div class="wrap">
  <div class="foot-row">
    <span class="label">The Two-Piece Edit — staging</span>
    <a href="index.html">Collection index</a>
  </div>
  <p>Staged locally at <code>/root/stage/twopiece</code>. Not published, not connected to Shopify or TeemDrop.
  Product data is supplier-sourced (TeemDrop SPUs) and has not been verified for retail; prices shown are
  proposed retail, unit costs are wholesale.</p>
</div></footer>
"""


def build_product(slug, idx):
    p = SPEC[slug]
    cols = colours_for(slug)
    imgs = IMAGES[slug]
    sizes = []
    for c in cols:
        for s in c[4]:
            if s not in sizes:
                sizes.append(s)
    sizes.sort(key=lambda s: ["S", "M", "L", "XL", "XXL"].index(s))

    default_img = cols[0][5] if cols[0][5] else imgs[0][0]
    data = {
        "slug": slug, "name": p["name"], "spu": p["spu"],
        "retail": RETAIL[slug], "cost": cost_str(slug),
        "sizes": sizes,
        "colours": [{"name": c[1], "sizes": c[4], "img": c[5] or ""} for c in cols],
    }

    thumbs = []
    for i, (src, alt) in enumerate(imgs):
        active = " is-active" if src == default_img else ""
        thumbs.append(
            '<button class="thumb%s" type="button" role="tab" aria-selected="%s" '
            'data-src="%s" data-alt="%s" aria-label="View image %d">'
            '<img src="%s" alt="" width="400" height="400" loading="%s"></button>'
            % (active, "true" if active else "false", src, alt, i + 1, src,
               "eager" if i < 2 else "lazy"))

    chips = []
    for i, c in enumerate(cols):
        chips.append(
            '<button class="chip chip-colour" type="button" aria-pressed="%s" '
            'data-colour="%s">%s<span>%s</span></button>'
            % ("true" if i == 0 else "false", i, swatch_html(c[2], c[3]), c[1]))

    facts = "\n".join("        <li>%s</li>" % b for b in BULLETS[slug])
    specs = "\n".join(
        '        <tr><th scope="row">%s</th><td>%s</td></tr>' % (k, v) for k, v in SPECS[slug])

    # related: next three in the capsule order
    related = []
    for k in range(1, 4):
        o = ORDER[(idx + k) % len(ORDER)]
        oi = IMAGES[o][0]
        related.append(
            '<a class="rel" href="%s.html">\n'
            '  <span class="rel-media"><img src="%s" alt="" width="300" height="375" loading="lazy"></span>\n'
            '  <span><h3>%s</h3><p>$%.2f · %d colourways</p></span>\n'
            '</a>' % (o, oi[0], SPEC[o]["name"], RETAIL[o], len(colours_for(o))))

    bread = '<div class="crumbs"><a href="index.html">The Two-Piece Edit</a><span class="sep">/</span><span>%s</span></div>' % p["name"]

    html = head("%s — The Two-Piece Edit (staging)" % p["name"], DESC[slug]) + "\n"
    html += '<a class="skip" href="#main">Skip to content</a>\n' + BAR + "\n" + HEADER + "\n"
    html += '<main id="main"><div class="wrap">\n' + bread + """
  <div class="product"><div class="p-grid">
    <section class="gallery" aria-label="Product images">
      <div class="frame">
        <img id="mainImg" src="%s" alt="%s" width="1000" height="1250">
      </div>
      <div class="thumbs" role="tablist" aria-label="Product image thumbnails">
        %s
      </div>
      <p class="frame-cap">Supplier photography · unretouched · staging only</p>
    </section>
    <section class="panel">
      <div class="eyebrow-row">
        <span class="label">Capsule 01 · Piece %02d</span>
        <span class="label">Staging</span>
      </div>
      <h1>%s</h1>
      <p class="spu">SPU %s · %d variants</p>
      <p class="price-note">%s</p>
      <div class="price-row">
        <span class="price">$%.2f</span>
        <span class="cost">unit cost %s</span>
      </div>
      <p class="price-note">Proposed retail, USD. Unit cost is the wholesale price per piece before freight.</p>

      <div class="field">
        <div class="field-head"><span class="label label-ink">Colourway</span><span class="val" id="pick"></span></div>
        <div class="chips" id="colours" role="group" aria-label="Colourway">
          %s
        </div>
      </div>

      <div class="field">
        <div class="field-head"><span class="label label-ink">Size</span><span class="val">%s</span></div>
        <div class="chips" id="sizes" role="group" aria-label="Size"></div>
        <p class="avail" id="avail"></p>
      </div>

      <ul class="facts">
%s
      </ul>

      <div class="cta" aria-disabled="true">Add to bag — staging preview only</div>

      <div class="notice">
        <strong>Staging page — not published.</strong> This page exists for internal review of range,
        colour and sizing. No cart, checkout or inventory sync is connected, and nothing here is
        listed on Shopify or TeemDrop.
      </div>

      <table class="mini-spec">
%s
        <tr><th scope="row">Colourways</th><td>%d</td></tr>
        <tr><th scope="row">Sizes</th><td>%s</td></tr>
        <tr><th scope="row">Variants</th><td>%d</td></tr>
      </table>
    </section>
  </div></div>

  <section class="related">
    <div class="sec-head"><h2>Also in the capsule</h2><span class="label">Three of six</span></div>
    <div class="rel-grid">
      %s
    </div>
  </section>
</div></main>
""" % (default_img, imgs[0][1], "\n        ".join(thumbs), idx + 1, p["name"],
       p["spu"], p["n_variants"], DESC[slug], RETAIL[slug], cost_str(slug),
       "\n          ".join(chips), " · ".join(sizes), facts, specs,
       len(cols), " · ".join(sizes), p["n_variants"], "\n      ".join(related))
    html += FOOTER
    html += '<script>window.PRODUCT = %s;</script>\n<script src="assets/site.js"></script>\n</body>\n</html>\n' % json.dumps(data)
    return html


def build_index():
    total_cost = 0.0
    total_retail = 0.0
    cards = []
    rows = []
    for i, slug in enumerate(ORDER):
        p = SPEC[slug]
        cols = colours_for(slug)
        sizes = []
        for c in cols:
            for s in c[4]:
                if s not in sizes:
                    sizes.append(s)
        sizes.sort(key=lambda s: ["S", "M", "L", "XL", "XXL"].index(s))
        total_cost += float(cost_str(slug).split(" – ")[0].replace("$", ""))
        total_retail += RETAIL[slug]
        seen, uniq = set(), []
        for c in cols:                       # dedupe: ls repeats colours across builds
            key = (c[2], c[3])
            if key in seen:
                continue
            seen.add(key)
            uniq.append(c)
        dots = "".join(swatch_html(c[2], c[3]) for c in uniq[:5])
        card_src, card_alt = CARD_IMG.get(slug, IMAGES[slug][0])
        cards.append("""      <article class="card%s">
        <a class="card-media" href="%s.html" aria-label="%s">
          <img src="%s" alt="%s" width="800" height="1000" loading="%s">
          <span class="card-idx num">%02d</span>
        </a>
        <h3><a href="%s.html">%s</a></h3>
        <div class="card-meta"><span class="card-price num">$%.2f</span><span class="label">%d colourways</span></div>
        <div class="card-sub"><span>%s</span><span class="swatches">%s</span></div>
        <a class="card-link" href="%s.html">View piece</a>
      </article>""" % (" alt" if i % 2 else "", slug, p["name"], card_src,
                       card_alt, "eager" if i < 3 else "lazy", i + 1, slug,
                       p["name"], RETAIL[slug], len(cols), " · ".join(sizes), dots, slug))

        rows.append("""        <tr>
          <td class="lead" data-label="Piece"><a href="%s.html">%s</a></td>
          <td data-label="SPU"><span class="t-spu">%s</span></td>
          <td data-label="Colourways" class="num">%d</td>
          <td data-label="Sizes">%s</td>
          <td data-label="Unit cost" class="num">%s</td>
          <td data-label="Retail" class="num">$%.2f</td>
        </tr>""" % (slug, p["name"], p["spu"], len(cols), " · ".join(sizes),
                     cost_str(slug), RETAIL[slug]))

    rows.append("""        <tr class="total">
          <td class="lead" data-label="Capsule">Six pieces</td>
          <td data-label="SPU">—</td>
          <td data-label="Colourways" class="num">%d</td>
          <td data-label="Sizes">S – XXL</td>
          <td data-label="Unit cost" class="num">$%.2f</td>
          <td data-label="Retail" class="num">$%.2f</td>
        </tr>""" % (sum(len(colours_for(s)) for s in ORDER), total_cost, total_retail))

    html = head("The Two-Piece Edit — six pieces (staging)",
                "Six-piece women's activewear capsule staged locally: colour-blocked two-piece sets, "
                "halter tops and wide-leg pants.") + "\n"
    html += '<a class="skip" href="#main">Skip to content</a>\n' + BAR + "\n" + HEADER + """
<main id="main">
  <section class="hero"><div class="wrap"><div class="hero-grid">
    <div class="hero-copy">
      <span class="label">Women's activewear · capsule 01</span>
      <h1>The Two-Piece <em>Edit</em></h1>
      <p class="lede">Six pieces cut from one idea: a colour-blocked waistband that reads as two garments and behaves as one.</p>
      <div class="hero-stats">
        <div><b class="num">06</b><span class="label">Pieces</span></div>
        <div><b class="num">%d</b><span class="label">Colourways</span></div>
        <div><b class="num">$%.2f</b><span class="label">Unit cost from</span></div>
      </div>
    </div>
    <div class="hero-media">
      <img src="assets/fauxset/colours/pomegranate-red-blue.jpg" alt="Faux Two-Piece Set: pomegranate bra with a blue wide-leg pant and cream contrast waistband" width="1200" height="1500" loading="eager">
    </div>
  </div></div></section>

  <section class="collection"><div class="wrap">
    <div class="sec-head"><h2>The six</h2><span class="label">Wine · powder blue · cream</span></div>
    <div class="cards">
%s
    </div>
  </div></section>

  <section class="spec-block" id="specs"><div class="wrap">
    <div class="sec-head"><h2>Spec sheet</h2><span class="label">Supplier data · unverified</span></div>
    <table class="spec">
      <thead><tr>
        <th scope="col">Piece</th><th scope="col">SPU</th><th scope="col" class="num">Colourways</th>
        <th scope="col">Sizes</th><th scope="col" class="num">Unit cost</th><th scope="col" class="num">Retail</th>
      </tr></thead>
      <tbody>
%s
      </tbody>
    </table>
    <p class="price-note">Unit cost is the TeemDrop wholesale price per piece in USD before freight and duties.
    Retail is the proposed price for this capsule, not a live store price. Sizes listed are the union across
    colourways — individual colourways run short, and each product page disables what is not available.</p>
  </div></section>
</main>
""" % (sum(len(colours_for(s)) for s in ORDER),
       min(float(cost_str(s).split(" – ")[0].replace("$", "")) for s in ORDER),
       "\n".join(cards), "\n".join(rows))
    html += FOOTER
    html += "</body>\n</html>\n"
    return html


if __name__ == "__main__":
    for i, slug in enumerate(ORDER):
        path = os.path.join(ROOT, slug + ".html")
        open(path, "w").write(build_product(slug, i))
        print("wrote", path)
    path = os.path.join(ROOT, "index.html")
    open(path, "w").write(build_index())
    print("wrote", path)

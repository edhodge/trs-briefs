#!/usr/bin/env python3
"""Render a TRS Live Brief page from a filled template + clip config.

Usage: python3 build_live_brief.py <config.json>

config.json:
{
  "template": "path/to/filled-template.html",   # template with {{CARDS_x}} + {{MEDMAP}} placeholders
  "slug": "c12-it-v3-sld-vid-towel-drill-vs-slider",  # lowercase-hyphenated card name, no date
  "assets": {"SYM": ["previewAssetId", "finalAssetId"], ...},  # from Recharm getClipLibrary sourceClipsAssetIds
  "drive":  {"SYM": "driveFileId", ...},        # original raw file per clip (Drive)
  "cards":  {"H1": [["SYM", "caption"], ...], ...}   # per-section clip cards
}

Clips stream from Recharm S3 (poster/preview = assets[0], lightbox final = assets[1]).
For the Claude-artifact WIP copy, embed base64 instead (artifact CSP blocks external hosts) —
see _engine/README.md.
"""
import json, os, sys

S3 = "https://recharm-content-library.s3-accelerate.amazonaws.com/trsgolf/clips/source"
RURL = "https://app.recharm.com/app/trsgolf/?clipId="

def main(cfg_path):
    cfg = json.load(open(cfg_path))
    assets, drive = cfg["assets"], cfg["drive"]

    def vid(sym, label):
        a0 = assets[sym][0]
        return (f'<div class="card" data-sym="{sym}" tabindex="0" role="button" aria-label="Preview {label}">'
                f'<video loop muted playsinline preload="metadata" poster="{S3}/poster/{a0}.jpg" '
                f'src="{S3}/preview/{a0}.mp4"></video>'
                f'<span>{label} · <a class="ext" href="{RURL}{sym}" target="_blank" rel="noopener">Recharm ↗</a>'
                f' · <a class="ext" href="https://drive.google.com/file/d/{drive[sym]}/view" target="_blank" rel="noopener">Drive ↗</a></span></div>')

    html = open(cfg["template"]).read()
    for key, items in cfg["cards"].items():
        html = html.replace("{{CARDS_" + key + "}}",
                            '<div class="cards">' + "".join(vid(s, l) for s, l in items) + "</div>")
    med = {s: f"{S3}/final/{a[1]}.mp4" for s, a in assets.items()}
    html = html.replace("{{MEDMAP}}", json.dumps(med))
    page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            '<link rel="icon" type="image/png" href="/favicon.png">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n</head>\n<body>\n' + html + "\n</body>\n</html>\n")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), cfg["slug"])
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w").write(page)
    print("built", os.path.join(out, "index.html"), f"({round(len(page)/1024)} KB)")

if __name__ == "__main__":
    main(sys.argv[1])

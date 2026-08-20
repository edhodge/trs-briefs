# Brief & Storyboard Engine

Renders TRS **Brief & Storyboard pages** — web versions of ad briefs where every script beat has its
source clips playing inline. Served at briefs.trsgolf.com (GitHub Pages, this repo).

- One folder per brief; slug = the Asana card name, lowercased and hyphenated, no date
  (e.g. `c12-it-v3-sld-vid-towel-drill-vs-slider/`). Old slugs keep a meta-refresh redirect stub.
- **Two templates, one per reader. Pick by who reads the page, not by whether a Loom exists.**
  - `template-creator-brief.html` — new shoot, the reader films it.
    Sections: Classification · Filming Instructions · Video Overview · Hooks To Film · Scenes · Extra B-Roll
  - `template-editor-brief.html` — footage exists, the reader cuts it.
    Sections: Classification · Delivery · Video Overview · Script Tags · Hooks To Cut · Scenes
  - Section names and order MIRROR the Google Doc templates in `01 | Ad Production`
    ([Template] | Creator Brief / [Template] | Editor Brief). If a section changes in the Doc it
    changes here, and vice versa. Do not add a section to one and not the other.
- `template-c12-example.html` — LEGACY, kept only because existing pages were built from it.
- `build_brief_storyboard.py` — fills {{CARDS_x}} + {{MEDMAP}} from a config; clips stream from
  Recharm S3 unsigned URLs. Never use `autoplay preload="auto"` on many clips (renderer stall);
  the template plays on-view via IntersectionObserver.
- WIP loop: iterate on a Claude artifact (base64-embedded media — artifact CSP blocks external
  hosts), push here only when Edward says so.
- The Google Doc brief stays the writable source of truth; these pages are generated views.
- Full workflow: VIDEO_BRIEF_BUILDER_SKILL.md ("Render the Brief & Storyboard" section) in
  Marketing/Creative Engine (TRS Golf repo).

## Drift Guard

Every build embeds `build <hash>` (template content hash) in the page footer. The Claude
artifact (WIP) and the live page must show the SAME stamp after a push — if they differ,
the live page is stale. "Push" always means: rebuild BOTH outputs from the current template,
publish both, confirm stamps match. No scheduled checker — the stamp makes the check free.

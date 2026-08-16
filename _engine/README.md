# Brief & Storyboard Engine

Renders TRS **Brief & Storyboard pages** — web versions of ad briefs where every script beat has its
source clips playing inline. Served at briefs.trsgolf.com (GitHub Pages, this repo).

- One folder per brief; slug = the Asana card name, lowercased and hyphenated, no date
  (e.g. `c12-it-v3-sld-vid-towel-drill-vs-slider/`). Old slugs keep a meta-refresh redirect stub.
- `template-c12-example.html` — the reference template (C12 content left in as a worked example).
  Structure: masthead (TRS | Ad Briefs) → card-name H1 → chips (Docs Brief / Folder / Asana /
  Recharm) → Upload Instructions → facts table (Asana naming order) → Previous Versions →
  Video Overview + Key → Hooks → Main Script blocks with {{CARDS_x}} clip slots → lightbox.
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

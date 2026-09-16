# www.kanavbengani.com

A single-page personal site. Cards orbit a centre card: **angle** encodes
category, **distance** encodes recency. `index.html` is self-contained — logos,
résumé preview and PDF are inlined.

```sh
python3 serve.py     # http://127.0.0.1:8787
python3 build.py     # regenerate index.html — run before deploying
```

**Editing** — only on localhost; other hosts never request `editor.js`. Hit
**Edit** (bottom-left) to drag, resize and rotate cards and labels, retype text,
or open a card's pencil for its modal content. **Save** writes `layout.json`
(positions) and `content.json` (copy); `build.py` bakes them in.

**Deploy** — GitHub Pages from the repo root. `editor.js` is git-ignored.

**Keys** — `W` work · `A` projects · `S` research · `D` education; again or
`Esc` to clear.

**Analytics** — GoatCounter, no cookies. Stats at
`kanavbengani.goatcounter.com`; set `GC_CODE = ""` in `build.py` to drop the tag
entirely. Pageviews are automatic; `track()` counts card opens, résumé
open/download, category filters and outbound clicks by host. Localhost never
reports, so events only show up from the deployed site.

`build.py` generates `index.html` and `editor.js`; edit `build.py` and
`_editor_src.js`, not the output.

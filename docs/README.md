# IDeaL project page

Self-contained project page for "IDeaL: Data-Free Multi-Teacher Distillation via
Improved Dead Leaves" (ECCV 2026). Everything (fonts, images, timelapse videos)
is inlined — `index.html` is the whole site.

## Files
- `index.html`            — the built page. Host this anywhere (GitHub Pages etc.). Open locally to preview.
- `ideal_page_template.html` — the SOURCE to edit. Same file, but with `%%img:key%%`,
                             `%%font:key%%` and `%%tl_json%%` placeholders instead of base64 blobs.
- `inject.py`             — build script: fills the placeholders from the *.json files.
- `images_b64.json`       — base64 JPEGs (sample pairs, ablation images, gaussian noise).
- `fonts_b64.json`        — Fraunces + Instrument Sans woff2 subsets.
- `videos_b64.json`       — timelapse MP4s (samples s0/s3/s4/s6, iterations 0→1000, 12 fps).
- `timelapse_meta.json`   — frame-index → iteration mapping used by the scrubber.
- `posters_b64.json`      — final-frame JPEG posters for the timelapse thumbnails.

## Editing
1. Edit `ideal_page_template.html` (all CSS/JS/copy lives there).
2. Rebuild:  `python inject.py`          # default samples: s3 s4 s6
   or        `python inject.py s3 s4 s6 s0`
3. Output: `ideal_page.html` (body-only, for Claude artifacts) and `index.html` (standalone).

To swap an image: re-encode a 224px JPEG to base64 and replace the value in
`images_b64.json`, or add a new key and reference it as `%%img:yourkey%%`.

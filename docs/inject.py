import json, re, sys
from pathlib import Path

S = Path(__file__).resolve().parent
imgs = json.load(open(S/'images_b64.json'))
fonts = json.load(open(S/'fonts_b64.json'))
vids = json.load(open(S/'videos_b64.json'))
meta = json.load(open(S/'timelapse_meta.json'))
posters = json.load(open(S/'posters_b64.json'))

# which timelapse samples appear in the player, per initialization source
CHOSEN = {'dl': ['s3', 's4', 's6'], 'gauss': ['g0', 'g1', 'g2']}
# sources whose assets are missing are dropped; the page hides their toggle
tl = {src: [{'v': vids[k], 'iters': meta[k], 'poster': posters[k]} for k in keys]
      for src, keys in CHOSEN.items() if all(k in vids for k in keys)}

html = open(S/'ideal_page_template.html').read()
html = html.replace('%%tl_json%%', json.dumps(tl))
def sub(m):
    kind, key = m.group(1), m.group(2)
    return (imgs if kind == 'img' else fonts)[key]
out = re.sub(r'%%(img|font):([\w]+)%%', sub, html)
assert '%%' not in out, 'leftover placeholder'
# everything before the marker (title, meta, structured data) belongs in <head>
if '<!-- /head -->' in out:
    head, body = out.split('<!-- /head -->', 1)
else:
    head, body = '<title>IDeaL</title>', out
head, body = head.strip(), body.strip()

# body-only version for Claude artifacts (title kept, meta stripped)
m = re.search(r'<title>.*?</title>', head)
title = m.group(0) if m else '<title>IDeaL</title>'
open(S/'ideal_page.html', 'w').write(title + '\n' + body + '\n')

# standalone version for GitHub Pages / self-hosting
standalone = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
              '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
              + head + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
if '--build-index' in sys.argv:
  open(S/'index.html', 'w').write(standalone)
print('size MB:', round(len(out)/1e6, 2))

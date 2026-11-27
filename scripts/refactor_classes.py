#!/usr/bin/env python3
"""Point-2 refactor: move CSS/JS hooks off data-pencil-name onto stable classes.

- Every element with data-pencil-name gets classes: pn, pn-<slug(name)>
  (plus pn-line when the name starts with "Line").
- Landmarks get semantic classes: header[Frame 12] -> site-header,
  nav[Frame 11] -> main-nav, main[Macbook 14"] -> page-frame, footer -> site-footer.
- Project card wrappers (Frame 8828..8833 in index/project) get project-card.
- The unnamed .project-title-wrap div in index/project gets named
  "Project title wrap" (safe now: card-specific hooks use .project-card).
- Selectors in css/*.css, js/*.js and in-page <style> blocks are rewritten:
  [data-pencil-name="X"] -> .pn-<slug>, Frame 12/11/Macbook -> semantic classes,
  [data-pencil-name^="Line"] -> .pn-line,
  .project-stack > [data-pencil-name] -> .project-stack > .project-card,
  any leftover bare [data-pencil-name] -> .pn
- data-pencil-name attributes stay in the HTML as documentation.
"""
import re, sys, glob, os, html as htmlmod

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "project.html", "experience.html", "contact.html",
         "mobile-pos.html", "dbank-pro.html", "upcademy.html",
         "waste4change.html", "niagahoster.html", "warunk-upnormal.html"]
CARD_NAMES = {f"Frame {n}" for n in range(8828, 8834)}
SEMANTIC = {"Frame 12": "site-header", "Frame 11": "main-nav", 'Macbook 14"': "page-frame"}

def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "x"

# ---------- collect all names, check slug collisions ----------
names = set()
for path in [os.path.join(REPO, p) for p in PAGES] + \
            [os.path.join(REPO, "css/style.css"), os.path.join(REPO, "css/responsive.css")] + \
            glob.glob(os.path.join(REPO, "js/*.js")):
    text = open(path).read()
    names |= {htmlmod.unescape(n) for n in re.findall(r'data-pencil-name="([^"]*)"', text)}
    names |= {htmlmod.unescape(n) for n in re.findall(r"data-pencil-name='([^']*)'", text)}
    names |= set(m.replace('\\"', '"') for m in re.findall(r'data-pencil-name=\\"([^"]*)\\"', text))
NAME2SLUG = {}
used = {}
for n in sorted(names):
    s = slugify(n)
    if s in used and used[s] != n:
        i = 2
        while f"{s}-{i}" in used:
            i += 1
        s = f"{s}-{i}"
    used[s] = n
    NAME2SLUG[n] = s
print(f"{len(names)} distinct names, slugs assigned (collisions suffixed)")

def slug(name):
    return NAME2SLUG[htmlmod.unescape(name)]

# ---------- selector rewriting (CSS/JS/style-block text) ----------
def rewrite_selectors(text, where):
    counts = {}
    def rep(pattern, repl, label):
        nonlocal text
        text, n = re.subn(pattern, repl, text)
        if n: counts[label] = counts.get(label, 0) + n
    # project-stack bare-attribute child selectors first
    rep(r'\.project-stack\s*>\s*\[data-pencil-name\]', '.project-stack > .project-card', 'stack-child')
    # semantic landmarks (both quote styles, CSS-escaped quote for Macbook)
    rep(r'\[data-pencil-name="Frame 12"\]', '.site-header', 'frame12')
    rep(r"\[data-pencil-name='Frame 12'\]", '.site-header', 'frame12')
    rep(r'\[data-pencil-name="Frame 11"\]', '.main-nav', 'frame11')
    rep(r"\[data-pencil-name='Frame 11'\]", '.main-nav', 'frame11')
    rep(r'\[data-pencil-name="Macbook 14\\"\]', '.page-frame', 'macbook')
    rep(r"\[data-pencil-name='Macbook 14\"'\]", '.page-frame', 'macbook')
    # prefix selector
    rep(r'\[data-pencil-name\^="Line"\]', '.pn-line', 'line-prefix')
    rep(r"\[data-pencil-name\^='Line'\]", '.pn-line', 'line-prefix')
    # generic exact-name selectors
    def gen(m):
        raw = m.group(1).replace('\\"', '"')
        counts['generic'] = counts.get('generic', 0) + 1
        return '.pn-' + slug(raw)
    text = re.sub(r'\[data-pencil-name="((?:[^"\\]|\\.)*)"\]', gen, text)
    text = re.sub(r"\[data-pencil-name='([^']*)'\]", gen, text)
    # leftover bare attribute selectors
    rep(r'\[data-pencil-name\]', '.pn', 'bare-leftover')
    if counts:
        print(f"  {where}: {counts}")
    return text

# ---------- HTML tag pass (parser-based: the export contains malformed
# attribute fragments like style="..."; margin: 0" that break regex tag
# matching, so tags are located with html.parser + get_starttag_text) ----
from html.parser import HTMLParser
CLASS_RE = re.compile(r'class\s*=\s*(?:"([^"]*)"|\'([^\']*)\')')

def add_classes(tag_text, tag, extra):
    m = CLASS_RE.search(tag_text)
    if m:
        cur = (m.group(1) if m.group(1) is not None else m.group(2)).split()
        add = [c for c in extra if c not in cur]
        if not add: return tag_text
        newval = " ".join(cur + add)
        q = '"' if m.group(1) is not None else "'"
        return tag_text[:m.start()] + f"class={q}{newval}{q}" + tag_text[m.end():]
    return "<" + tag + f' class="{" ".join(extra)}"' + tag_text[len(tag) + 1:]

class TagIndex(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.line_starts = [0] + [m.end() for m in re.finditer("\n", text)]
        self.tags = []  # (offset, raw, tag, attrs-dict)
    def _record(self, tag, attrs):
        raw = self.get_starttag_text()
        line, col = self.getpos()
        off = self.line_starts[line - 1] + col
        self.tags.append((off, raw, tag, dict(attrs)))
    handle_starttag = _record
    handle_startendtag = _record

def html_pass(text, fname):
    stats = {"named": 0, "semantic": 0, "cards": 0}
    idx = TagIndex(text)
    idx.feed(text)
    edits = []
    for off, raw, tag, attrs in idx.tags:
        assert text[off:off + len(raw)] == raw, f"{fname}: offset mismatch at {off}"
        name = attrs.get("data-pencil-name")
        if name is None:
            if tag == "footer":
                edits.append((off, raw, add_classes(raw, tag, ["site-footer"])))
                stats["semantic"] += 1
            continue
        extra = ["pn", "pn-" + slug(name)]
        if name.startswith("Line"): extra.append("pn-line")
        if (tag == "header" and name == "Frame 12") or \
           (tag == "nav" and name == "Frame 11") or \
           (tag == "main" and name == 'Macbook 14"'):
            extra.append(SEMANTIC[name]); stats["semantic"] += 1
        if tag == "footer": extra.append("site-footer"); stats["semantic"] += 1
        if fname in ("index.html", "project.html") and name in CARD_NAMES:
            extra.append("project-card"); stats["cards"] += 1
        stats["named"] += 1
        new = add_classes(raw, tag, extra)
        if new != raw: edits.append((off, raw, new))
    for off, raw, new in sorted(edits, reverse=True):
        text = text[:off] + new + text[off + len(raw):]
    # name the project title wrap (index/project only)
    if fname in ("index.html", "project.html"):
        old = '<div class="project-title-wrap">'
        assert text.count(old) == 1, f"{fname}: title wrap count {text.count(old)}"
        text = text.replace(old, '<div data-pencil-name="Project title wrap" class="project-title-wrap pn pn-project-title-wrap">')
        stats["named"] += 1
    print(f"  {fname}: {stats}")
    return text

for p in PAGES:
    path = os.path.join(REPO, p)
    text = open(path).read()
    text = rewrite_selectors(text, p + " <style>")
    text = html_pass(text, p)
    open(path, "w").write(text)

for css in ["css/style.css", "css/responsive.css"]:
    path = os.path.join(REPO, css)
    css_text = open(path).read()
    with open(path, "w") as fh:
        fh.write(rewrite_selectors(css_text, css))

for js in ["js/main.js", "js/mobile-nav.js", "js/burjo-carousel.js", "js/phone-strip-dots.js"]:
    path = os.path.join(REPO, js)
    text = rewrite_selectors(open(path).read(), js)
    text = text.replace('wrap.hasAttribute("data-pencil-name")', 'wrap.classList.contains("project-card")')
    open(path, "w").write(text)

print("done")

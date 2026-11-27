#!/usr/bin/env python3
"""Point-1 refactor: extract repeated inline styles into shared classes.

- Collects every inline style string across the 10 pages (parser-based).
- Strings used >= 3 times become utility classes .u1, .u2, ... in
  css/utilities.css, which every page loads AFTER responsive.css.
- Safety filter (all-or-nothing per string): a string is extracted only if
  EVERY element carrying it passes:
  * the element is not inside an SVG subtree;
  * no CSS rule that mentions one of the element's classes (or its id)
    sets an overlapping property to a different value without !important
    (rules that already win via !important, or set the same value, are safe;
    :has(...) parent segments are ignored since they target the parent).
- The raw style attribute must be locatable verbatim in the tag text.
- Audit: total declaration count before == after (inline + class-borne).
"""
import re, os, glob, html as htmlmod
from html.parser import HTMLParser
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "project.html", "experience.html", "contact.html",
         "mobile-pos.html", "dbank-pro.html", "upcademy.html",
         "waste4change.html", "niagahoster.html", "warunk-upnormal.html"]
MIN_USES = 3

SHORTHANDS = {
    "margin": {"margin-top", "margin-right", "margin-bottom", "margin-left"},
    "padding": {"padding-top", "padding-right", "padding-bottom", "padding-left"},
    "background": {"background-color", "background-image", "background-position",
                   "background-size", "background-repeat", "background-attachment"},
    "border": {"border-width", "border-style", "border-color",
               "border-top", "border-right", "border-bottom", "border-left"},
    "font": {"font-family", "font-size", "font-weight", "font-style", "line-height"},
    "flex": {"flex-grow", "flex-shrink", "flex-basis"},
    "overflow": {"overflow-x", "overflow-y"},
    "inset": {"top", "right", "bottom", "left"},
    "transition": {"transition-property", "transition-duration",
                   "transition-timing-function", "transition-delay"},
}

def props_overlap(a, b):
    if a == b: return True
    if a in SHORTHANDS and b in SHORTHANDS[a]: return True
    if b in SHORTHANDS and a in SHORTHANDS[b]: return True
    return False

def norm(s):
    return re.sub(r"\s+", " ", s.strip().rstrip(";")).strip()

def parse_decls(body):
    out = {}
    for part in body.split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip().lower()] = re.sub(r"\s+", " ", v.strip().lower())
    return out

# ---------- gather CSS rules ----------
rules = []  # (selector_text_without_has, decls{prop:(value, important)})
css_texts = [open(os.path.join(REPO, "css/style.css")).read(),
             open(os.path.join(REPO, "css/responsive.css")).read()]
for p in PAGES:
    css_texts += re.findall(r"<style[^>]*>(.*?)</style>", open(os.path.join(REPO, p)).read(), re.S)
for css in css_texts:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel = re.sub(r":has\([^)]*\)", "", m.group(1))
        decls = {}
        for part in m.group(2).split(";"):
            if ":" in part:
                k, v = part.split(":", 1)
                v = v.strip()
                imp = v.lower().endswith("!important")
                decls[k.strip().lower()] = (re.sub(r"\s+", " ", v.lower().replace("!important", "").strip()), imp)
        if decls:
            rules.append((sel, decls))
print(f"{len(rules)} CSS rules in the conflict scan")

def conflicts(classes, el_id, inline_decls):
    bad = []
    for sel, decls in rules:
        mentioned = set(re.findall(r"\.([a-zA-Z0-9_-]+)", sel))
        idm = set(re.findall(r"#([a-zA-Z0-9_-]+)", sel))
        if not (mentioned & set(classes)) and not (el_id and el_id in idm):
            continue
        for prop, val in inline_decls.items():
            for rprop, (rval, imp) in decls.items():
                if imp: continue
                if props_overlap(prop, rprop) and rval != val:
                    bad.append((sel.strip()[:60], rprop, rval, val))
                    return bad
    return bad

# ---------- locate styled elements ----------
class TagIndex(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.line_starts = [0] + [m.end() for m in re.finditer("\n", text)]
        self.tags = []
        self.svg_depth = 0
    def _record(self, tag, attrs, selfclosing=False):
        raw = self.get_starttag_text()
        line, col = self.getpos()
        off = self.line_starts[line - 1] + col
        self.tags.append((off, raw, tag, dict(attrs), self.svg_depth > 0 or tag == "svg"))
        if tag == "svg" and not selfclosing:
            self.svg_depth += 1
    def handle_starttag(self, tag, attrs):
        self._record(tag, attrs)
    def handle_startendtag(self, tag, attrs):
        self._record(tag, attrs, selfclosing=True)
    def handle_endtag(self, tag):
        if tag == "svg" and self.svg_depth > 0:
            self.svg_depth -= 1

page_tags = {}
counts = Counter()
for p in PAGES:
    text = open(os.path.join(REPO, p)).read()
    idx = TagIndex(text)
    idx.feed(text)
    page_tags[p] = (text, idx.tags)
    for off, raw, tag, attrs, in_svg in idx.tags:
        if "style" in attrs:
            counts[norm(attrs["style"])] += 1

candidates = {s: c for s, c in counts.items() if c >= MIN_USES}
print(f"{len(candidates)} candidate strings (>={MIN_USES} uses)")

STYLE_ATTR_RE = re.compile(r'(?<![-\w])style\s*=\s*(?:"([^"]*)"|\'([^\']*)\')')
CLASS_RE = re.compile(r'class\s*=\s*(?:"([^"]*)"|\'([^\']*)\')')

def add_class(tag_text, tag, cls):
    m = CLASS_RE.search(tag_text)
    if m:
        cur = (m.group(1) if m.group(1) is not None else m.group(2)).split()
        if cls in cur: return tag_text
        q = '"' if m.group(1) is not None else "'"
        return tag_text[:m.start()] + f"class={q}{' '.join(cur + [cls])}{q}" + tag_text[m.end():]
    return "<" + tag + f' class="{cls}"' + tag_text[len(tag) + 1:]

# decide per string: every carrier must pass
string_ok = {}
for s in candidates:
    decls = parse_decls(s)
    ok = True
    for p in PAGES:
        text, tags = page_tags[p]
        for off, raw, tag, attrs, in_svg in tags:
            if "style" not in attrs or norm(attrs["style"]) != s:
                continue
            if in_svg: ok = False; break
            m = STYLE_ATTR_RE.search(raw)
            rawval = None
            if m:
                rawval = m.group(1) if m.group(1) is not None else m.group(2)
            if rawval is None or htmlmod.unescape(rawval) != attrs["style"]:
                ok = False; break
            if conflicts(attrs.get("class", "").split(), attrs.get("id"), decls):
                ok = False; break
        if not ok: break
    string_ok[s] = ok

extract = sorted([s for s, ok in string_ok.items() if ok], key=lambda s: -counts[s])
skipped = [s for s, ok in string_ok.items() if not ok]
print(f"extracting {len(extract)} strings, keeping {len(skipped)} inline (safety filter)")
uclass = {s: f"u{i+1}" for i, s in enumerate(extract)}

# audit: declarations before
before = 0
for p in PAGES:
    text, tags = page_tags[p]
    for off, raw, tag, attrs, in_svg in tags:
        if "style" in attrs:
            before += len(parse_decls(attrs["style"]))

# apply edits
converted = 0
for p in PAGES:
    path = os.path.join(REPO, p)
    text, tags = page_tags[p]
    edits = []
    for off, raw, tag, attrs, in_svg in tags:
        if "style" not in attrs: continue
        s = norm(attrs["style"])
        if s not in uclass: continue
        assert text[off:off + len(raw)] == raw
        m = STYLE_ATTR_RE.search(raw)
        new = raw[:m.start()] + raw[m.end():]
        new = re.sub(r" {2,}(?=>)", " ", new)  # tidy double space before >
        new = add_class(new, tag, uclass[s])
        edits.append((off, raw, new))
        converted += 1
    for off, raw, new in sorted(edits, reverse=True):
        text = text[:off] + new + text[off + len(raw):]
    # load utilities.css last
    anchor = '<link rel="stylesheet" href="css/responsive.css" />'
    assert text.count(anchor) == 1, f"{p}: stylesheet anchor count {text.count(anchor)}"
    text = text.replace(anchor, anchor + '\n    <link rel="stylesheet" href="css/utilities.css" />')
    with open(path, "w") as fh:
        fh.write(text)
    print(f"  {p}: {len(edits)} elements converted")

# write utilities.css
lines = ["/* Shared utility classes extracted from repeated inline styles",
         "   by scripts/extract_styles.py (point-1 refactor). Loaded last;",
         "   do not edit by hand, regenerate instead. */", ""]
for s in extract:
    lines.append(f".{uclass[s]} {{ {s}; }}")
with open(os.path.join(REPO, "css/utilities.css"), "w") as fh:
    fh.write("\n".join(lines) + "\n")

# audit: declarations after
after = 0
for p in PAGES:
    text = open(os.path.join(REPO, p)).read()
    idx = TagIndex(text)
    idx.feed(text)
    for off, raw, tag, attrs, in_svg in idx.tags:
        if "style" in attrs:
            after += len(parse_decls(attrs["style"]))
        for c in attrs.get("class", "").split():
            if c in uclass.values():
                s = next(k for k, v in uclass.items() if v == c)
                after += len(parse_decls(s))
print(f"declarations before: {before} | after: {after} | {'MATCH' if before == after else 'MISMATCH!'}")
print(f"converted elements: {converted}")

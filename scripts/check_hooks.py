#!/usr/bin/env python3
"""Verify the class-hook refactor invariants for the Kinanti portfolio site.

Fails (exit 1) when any of these break:
  1. A data-pencil-name selector survives in css/, js/ or an in-page <style>.
  2. An element carries data-pencil-name without the pn / pn-* classes.
  3. A page does not have exactly one .site-header, .main-nav and
     .site-footer (and exactly one .page-frame, except contact.html which
     has no <main> by design).
  4. A pn-* class referenced from CSS/JS exists on no page.
  5. A .project-stack card wrapper lacks .project-card, or the title wrap
     has it (the mobile rules and the scroll animation key off it).

Run from the repo root:  python3 scripts/check_hooks.py
"""
import glob, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "project.html", "experience.html", "contact.html",
         "mobile-pos.html", "dbank-pro.html", "upcademy.html",
         "waste4change.html", "niagahoster.html", "warunk-upnormal.html"]
NO_MAIN = {"contact.html"}
errors = []

class Audit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.land = {}
        self.stack_depth = None
        self.depth = 0
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        cls = d.get("class", "").split()
        if "data-pencil-name" in d:
            if "pn" not in cls or not any(c.startswith("pn-") for c in cls):
                errors.append(f"named element without pn classes: <{tag}> {d['data-pencil-name']!r}")
        for c in ("site-header", "main-nav", "page-frame", "site-footer"):
            if c in cls:
                self.land[c] = self.land.get(c, 0) + 1
        if "project-stack" in cls:
            self.stack_depth = self.depth
        elif self.stack_depth is not None and self.depth == self.stack_depth + 1:
            if "project-title-wrap" in cls and "project-card" in cls:
                errors.append("project title wrap must not carry project-card")
            if "data-pencil-name" in d and "project-title-wrap" not in cls \
               and "project-card" not in cls:
                errors.append(f"project-stack card without project-card: {d['data-pencil-name']!r}")
        if tag not in ("img", "br", "meta", "link", "input", "hr", "source"):
            self.depth += 1
    handle_startendtag = handle_starttag
    def handle_endtag(self, tag):
        if tag not in ("img", "br", "meta", "link", "input", "hr", "source"):
            self.depth -= 1
        if self.stack_depth is not None and self.depth == self.stack_depth:
            self.stack_depth = None

present = set()
for page in PAGES:
    text = open(os.path.join(ROOT, page)).read()
    for style in re.findall(r"<style[^>]*>(.*?)</style>", text, re.S):
        if "data-pencil-name" in style:
            errors.append(f"{page}: data-pencil-name selector inside <style>")
    for m in re.finditer(r'class="([^"]*)"', text):
        present |= {c for c in m.group(1).split() if c.startswith("pn-")}
    a = Audit()
    a.feed(text)
    for c in ("site-header", "main-nav", "site-footer"):
        if a.land.get(c, 0) != 1:
            errors.append(f"{page}: expected exactly 1 .{c}, found {a.land.get(c, 0)}")
    want_main = 0 if page in NO_MAIN else 1
    if a.land.get("page-frame", 0) != want_main:
        errors.append(f"{page}: expected {want_main} .page-frame, found {a.land.get('page-frame', 0)}")

refs = set()
for path in ["css/style.css", "css/responsive.css"] + glob.glob(os.path.join(ROOT, "js/*.js")):
    text = open(path).read()
    if "data-pencil-name" in text and path.endswith((".css", ".js")):
        if re.search(r"\[data-pencil-name", text):
            errors.append(f"{os.path.relpath(path, ROOT)}: data-pencil-name selector remains")
    refs |= set(re.findall(r"\.(pn-[a-z0-9-]+)", text))
for c in sorted(refs - present):
    errors.append(f"CSS/JS references .{c} but no page element carries it")

if errors:
    print("check_hooks: FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"check_hooks: OK ({len(PAGES)} pages, {len(refs)} pn classes referenced)")

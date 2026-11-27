# How this site is built

The pages in this repo are **build outputs**. The site started as a Pencil
export (nested divs, inline styles, `data-pencil-name` attributes), and every
structural change since then was made by a small script that asserts what it
expects to find before it writes. Keep it that way: change the script or the
shell, rebuild, verify, then push. Do not hand-edit the generated pages.

## The hook system (since the 2026-11-27 refactor)

CSS and JS never select on `data-pencil-name` anymore. That attribute stays
in the HTML as documentation only. Hooks are classes:

- `pn` + `pn-<slug>` on every named element, one class per Pencil name
  (slug = the name lowercased, non-alphanumerics collapsed to `-`).
- Landmarks: `.site-header` (the fixed navbar), `.main-nav`, `.page-frame`
  (the `<main>`), `.site-footer`.
- `.project-card` on the six project card wrappers inside `.project-stack`
  in index.html and project.html. The mobile stacking rules and the scroll
  animation key off this class, which is why the section title wrap above
  the cards must never carry it.
- `.pn-line` on SVG elements whose Pencil name starts with "Line".
- `.u1` ... `.u111` in `css/utilities.css`: inline styles that repeated
  across pages, extracted into shared classes. That file is generated.

## Verification gate

Before any push:

```
python3 scripts/check_hooks.py
```

It fails if a `data-pencil-name` selector survives anywhere, if a named
element lost its `pn` classes, if a landmark class is missing or doubled,
if CSS/JS references a `pn-*` class no page carries, or if the project
stack card marking is wrong.

## Rebuilding the case study pages

The six case study pages (mobile-pos, dbank-pro, upcademy, waste4change,
niagahoster, warunk-upnormal) are assembled by `scripts/build_pages.py`
from:

- `scripts/shell/prefix.html` — doctype, head, header, up to and including
  the `<main>` start tag. Re-extracted from the current project.html on
  2026-11-27, after the class refactor.
- `scripts/shell/footer.html` — the shared footer block (byte-identical on
  all six pages), re-extracted from dbank-pro.html the same day.
- `scripts/shell/suffix.html` — `</main>` plus everything after the footer.
- `scripts/shell/header.html` — empty; the header lives inside the prefix.
- The article bodies, which live as string literals inside build_pages.py.
  Their source briefs are in `scripts/briefs/`.

Pipeline after a rebuild, in this order:

```
python3 scripts/build_pages.py        # assemble the six pages
python3 scripts/rename_divs.py        # name any unnamed divs (documentation)
python3 scripts/refactor_classes.py   # re-apply pn / landmark classes
python3 scripts/extract_styles.py     # regenerate css/utilities.css
python3 scripts/check_hooks.py        # must pass
```

A rebuild from the current shell reproduces the live pages except for the
documentation names on article divs (restored by rename_divs.py) and minor
whitespace around `</main>`.

## Regenerating the structure page

`structure.html` (published as /structure) is a copy of index.html with an
inspection layer injected by `scripts/build_structure.py`. Never edit it
directly; re-run the script after any change to index.html:

```
python3 scripts/build_structure.py
```

## Script inventory

| Script | Role |
| --- | --- |
| `build_pages.py` | Assemble the six case study pages from the shell |
| `build_structure.py` | Regenerate structure.html from index.html |
| `check_hooks.py` | Verification gate described above |
| `extract_styles.py` | Regenerate css/utilities.css from repeated inline styles |
| `refactor_classes.py` | The 2026-11-27 point-2 transform (attribute selectors to classes) |
| `rename_divs.py` | Give every unnamed div a data-pencil-name from its content |
| `rebuild_chrome.py` | Historical: semantic header/nav/footer rebuild |
| `fix_semantics.py` | Historical: landmarks, one h1 per page, alts, lang, meta |

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give every unnamed <div> a data-pencil-name, on all 10 Kinanti pages.

Names are derived, in order: first class (humanized), id (humanized), the
first phrase of the element's own text, or the nearest named ancestor plus
"inner". Names are made unique per page with a numeric suffix.

DELIBERATE EXCEPTION: direct children of a .project-stack container are NOT
named. css/responsive.css and css/style.css carry rules scoped as
".project-stack > [data-pencil-name]" that restyle those children on small
screens; giving them the attribute would change the mobile layout. Naming
them belongs with the point-2 selector refactor (stable classes) instead.
"""
import re
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
PAGES = ['index.html', 'experience.html', 'project.html', 'contact.html',
         'mobile-pos.html', 'dbank-pro.html', 'upcademy.html', 'waste4change.html',
         'niagahoster.html', 'warunk-upnormal.html']
VOID = {'meta', 'link', 'img', 'br', 'hr', 'input', 'source'}
WORDMAP = {'cs': 'Case study', 'asa': 'ASA', 'ui': 'UI', 'ux': 'UX'}


def parse(src):
    lines = src.split('\n')
    off = [0]
    for L in lines:
        off.append(off[-1] + len(L) + 1)

    def pos(p):
        return off[p[0] - 1] + p[1]

    class P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.stack = []
            self.elems = []

        def _mk(self, tag, attrs, s, raw):
            return {'tag': tag, 'attrs': dict(attrs), 'start': s,
                    'tagend': s + len(raw), 'end': None,
                    'parent': self.stack[-1] if self.stack else None, 'own': ''}

        def handle_starttag(self, tag, attrs):
            s = pos(self.getpos())
            raw = self.get_starttag_text() or ''
            el = self._mk(tag, attrs, s, raw)
            self.elems.append(el)
            if tag not in VOID:
                self.stack.append(el)
            else:
                el['end'] = el['tagend']

        def handle_startendtag(self, tag, attrs):
            s = pos(self.getpos())
            raw = self.get_starttag_text() or ''
            el = self._mk(tag, attrs, s, raw)
            el['end'] = el['tagend']
            self.elems.append(el)

        def handle_data(self, d):
            if self.stack:
                self.stack[-1]['own'] += d

        def handle_endtag(self, tag):
            e = pos(self.getpos())
            gt = src.find('>', e)
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i]['tag'] == tag:
                    self.stack[i]['end'] = gt + 1
                    if i > 0:
                        self.stack[i - 1]['own'] += self.stack[i]['own']
                    del self.stack[i:]
                    break

    p = P()
    p.feed(src)
    return p.elems


def humanize(token):
    words = re.split(r'[-_]+', token.strip())
    out = []
    for i, w in enumerate(words):
        if not w:
            continue
        lw = w.lower()
        if lw in WORDMAP:
            out.append(WORDMAP[lw])
        elif i == 0:
            out.append(w[:1].upper() + w[1:])
        else:
            out.append(w)
    return ' '.join(out).strip()


def text_phrase(el):
    t = re.sub(r'\s+', ' ', el['own']).strip()
    if not t:
        return None
    seg = re.split(r'[·:—|]', t)[0].strip()
    words = [w for w in re.split(r'\s+', seg) if re.search(r'[A-Za-z0-9]', w)][:4]
    if not words:
        return None
    name = ' '.join(words)
    name = re.sub(r'[^A-Za-z0-9 /&+-]', '', name).strip()
    if not name:
        return None
    return name[:1].upper() + name[1:]


def nearest_named_ancestor(el, assigned):
    p = el['parent']
    while p is not None:
        nm = assigned.get(id(p)) or p['attrs'].get('data-pencil-name')
        if nm:
            return nm
        p = p['parent']
    return None


for fname in PAGES:
    path = REPO + fname
    src = open(path, encoding='utf-8').read()
    els = parse(src)
    used = {e['attrs']['data-pencil-name'] for e in els if 'data-pencil-name' in e['attrs']}
    assigned = {}
    edits = []
    renamed = skipped = 0
    for e in els:
        if e['tag'] != 'div' or 'data-pencil-name' in e['attrs']:
            continue
        parent = e['parent']
        if parent is not None and 'project-stack' in (parent['attrs'].get('class') or ''):
            skipped += 1
            continue
        cls = (e['attrs'].get('class') or '').split()
        base = None
        if cls:
            base = humanize(cls[0])
        if not base and e['attrs'].get('id'):
            base = humanize(e['attrs']['id'])
        if not base:
            base = text_phrase(e)
        if not base:
            anc = nearest_named_ancestor(e, assigned)
            base = (anc + ' inner') if anc else 'Div'
        name = base
        n = 2
        while name in used:
            name = f'{base} {n}'
            n += 1
        used.add(name)
        assigned[id(e)] = name
        edits.append((e['start'], e['start'] + 4, f'<div data-pencil-name="{name}"'))
        renamed += 1
    for s, e_, rep in sorted(edits, key=lambda x: x[0], reverse=True):
        src = src[:s] + rep + src[e_:]
    open(path, 'w', encoding='utf-8').write(src)

    els2 = parse(src)
    divs = [e for e in els2 if e['tag'] == 'div']
    left = [e for e in divs if 'data-pencil-name' not in e['attrs']]
    unclosed = sum(1 for e in els2 if e['end'] is None)
    print(f'{fname}: renamed={renamed} skipped(project-stack)={skipped} unnamed-left={len(left)} unclosed={unclosed}')
    assert len(left) == skipped and unclosed == 0

print('RENAME DONE')

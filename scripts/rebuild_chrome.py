# -*- coding: utf-8 -*-
"""Semantic + accessibility rebuild of the Kinanti site navbar and footer.

- Frame 12 bar  -> <header>, Frame 11 link row -> <nav aria-label="Main"> with a list,
  logo gets role="img" + label, decorative SVGs get aria-hidden.
- div#contact frame -> <footer id="contact">: headline becomes <h2>, Explore row becomes
  <nav> with a list, clock becomes <time>, social links get aria-labels, SVGs aria-hidden.
- Pages that only had the small explore+clock footer get the full footer frame,
  placed after the Macbook frame exactly like on the home page.
Visual styles are copied verbatim from the existing markup; JS hooks
(data-pencil-name Frame 11/12, data-live-clock, #contact, .contact-blue-sticker) are kept.
"""
import re
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
VOID = {'meta', 'link', 'img', 'br', 'hr', 'input', 'source'}

STYLE_BLOCK = ('<style>\n'
               '[data-pencil-name="Frame 12"] a:focus-visible, #contact a:focus-visible '
               '{ outline: 3px solid #2185e3; outline-offset: 3px; border-radius: 6px; }\n'
               '</style>\n')


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
                    'parent': self.stack[-1] if self.stack else None}

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

        def handle_endtag(self, tag):
            e = pos(self.getpos())
            gt = src.find('>', e)
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i]['tag'] == tag:
                    self.stack[i]['end'] = gt + 1
                    del self.stack[i:]
                    break

    p = P()
    p.feed(src)
    return p.elems


def by_name(elems, name):
    return next(el for el in elems if el['attrs'].get('data-pencil-name') == name)


def apply_edits(src, edits):
    """edits: list of (start, end, replacement), applied back to front."""
    for s, e, rep in sorted(edits, key=lambda x: x[0], reverse=True):
        src = src[:s] + rep + src[e:]
    return src


def hide_svgs(segment):
    n = len(re.findall(r'<svg', segment))
    segment = re.sub(r'<svg(?![^>]*aria-hidden)', '<svg aria-hidden="true" focusable="false"', segment)
    return segment, n


# ---------------------------------------------------------------- header
def transform_header(doc):
    elems = parse(doc)
    f12 = by_name(elems, 'Frame 12')
    seg = doc[f12['start']:f12['end']]
    sub = parse(seg)
    edits = []

    # Frame 11 -> nav with list, reusing the original anchors verbatim
    f11 = by_name(sub, 'Frame 11')
    anchors = [el for el in sub if el['tag'] == 'a' and f11['start'] <= el['start'] and el['end'] <= f11['end']]
    assert len(anchors) == 3, f'header anchors: {len(anchors)}'
    lis = ''.join(f'<li>{seg[a["start"]:a["end"]]}</li>' for a in anchors)
    nav = (f'<nav data-pencil-name="Frame 11" aria-label="Main" '
           f'style="{f11["attrs"].get("style", "")}">'
           f'<ul style="align-items: center; box-sizing: border-box; display: flex; flex-direction: row; '
           f'gap: 32px; list-style: none; margin: 0; padding: 0">{lis}</ul></nav>')
    edits.append((f11['start'], f11['end'], nav))

    # logo gets an accessible name
    logo = by_name(sub, 'logo')
    edits.append((logo['tagend'] - 1, logo['tagend'] - 1, ' role="img" aria-label="Kinanti"'))

    seg = apply_edits(seg, edits)
    seg, nsvg = hide_svgs(seg)
    assert nsvg == 7, f'header svgs: {nsvg}'
    # Frame 12 -> header
    assert seg.startswith('<div')
    seg = '<header' + seg[4:]
    assert seg.rstrip().endswith('</div>')
    seg = seg.rstrip()[:-len('</div>')] + '</header>'
    return doc[:f12['start']] + seg + doc[f12['end']:]


# ---------------------------------------------------------------- footer frame
EXPLORE_BOX_STYLE = ('align-items: flex-start; box-sizing: border-box; display: flex; flex-direction: column; '
                     'flex-shrink: 0; gap: 16px; height: fit-content; justify-content: flex-start; '
                     'position: relative; width: fit-content; z-index: 2')
EXPLORE_LABEL_STYLE = ('box-sizing: border-box; color: #363636ff; font-family: Silkscreen, system-ui, sans-serif; '
                       'font-size: 20px; font-style: normal; font-weight: 700; letter-spacing: 0px; '
                       'line-height: normal; text-align: left; white-space: nowrap')
EXPLORE_LINK_STYLE = ('box-sizing: border-box; color: #4e4e4eff; font-family: "DM Sans", system-ui, sans-serif; '
                      'font-size: 20px; font-style: normal; font-weight: 500; letter-spacing: 0px; '
                      'line-height: normal; text-align: left; white-space: nowrap; text-decoration: none')
SOCIAL_LABELS = {
    'https://www.linkedin.com/in/kinanti-ayudya-putri-rahardiani/': 'Kinanti Ayudya Putri Rahardiani on LinkedIn',
    'https://www.instagram.com/kaputrir/': 'Kinanti on Instagram (@kaputrir)',
    'https://dribbble.com/kaputrir': 'Kinanti on Dribbble (kaputrir)',
    'https://medium.com/@kaputrir': 'Kinanti on Medium (@kaputrir)',
}
NAV_PAGES = [('Home', 'index.html'), ('Experience', 'experience.html'),
             ('Project', 'project.html'), ('Contact', 'contact.html')]


def build_footer_frame(current, own_file):
    import subprocess
    src = subprocess.run(['git', '-C', REPO, 'show', 'HEAD:index.html'],
                         capture_output=True, text=True, check=True).stdout
    elems = parse(src)
    frame = next(el for el in elems if el['attrs'].get('id') == 'contact')
    seg = src[frame['start']:frame['end']]
    sub = parse(seg)
    edits = []

    # headline -> h2 (keep style, add margin reset)
    h = by_name(sub, 'Have a question or just want to say hi?')
    stag = seg[h['start']:h['tagend']]
    stag = '<h2' + stag[len('<div'):]
    stag = re.sub(r'style="([^"]*)"', lambda m: f'style="{m.group(1)}; margin: 0"', stag, count=1)
    edits.append((h['start'], h['tagend'], stag))
    edits.append((h['end'] - len('</div>'), h['end'], '</h2>'))

    # explore row -> nav with list
    ex = by_name(sub, 'explore')
    items = []
    for label, href in NAV_PAGES:
        cur = ' aria-current="page"' if href == own_file else ''
        items.append(f'<li><a data-pencil-name="{label}" href="{href}"{cur} '
                     f'style=\'{EXPLORE_LINK_STYLE}\'>{label}</a></li>')
    nav = (f'<nav data-pencil-name="explore" aria-labelledby="kp-explore-label" style="{EXPLORE_BOX_STYLE}">'
           f'<div id="kp-explore-label" data-pencil-name="Explore" style="{EXPLORE_LABEL_STYLE}">Explore</div>'
           f'<ul style="display: flex; flex-direction: column; gap: 16px; list-style: none; margin: 0; padding: 0">'
           + ''.join(items) + '</ul></nav>')
    edits.append((ex['start'], ex['end'], nav))

    # clock -> time
    clock = next(el for el in sub if 'data-live-clock' in el['attrs'])
    ctag = seg[clock['start']:clock['tagend']]
    edits.append((clock['start'], clock['tagend'], '<time' + ctag[len('<div'):]))
    edits.append((clock['end'] - len('</div>'), clock['end'], '</time>'))

    # social links get explicit labels
    for el in sub:
        if el['tag'] == 'a' and el['attrs'].get('href') in SOCIAL_LABELS:
            edits.append((el['start'] + 2, el['start'] + 2,
                          f' aria-label="{SOCIAL_LABELS[el["attrs"]["href"]]}"'))

    # back to top points at the page itself
    btt = by_name(sub, 'Tertiary button')
    btag = seg[btt['start']:btt['tagend']]
    nbtag = btag.replace('href="index.html"', f'href="{own_file}"')
    if own_file != 'index.html':
        assert nbtag != btag
    edits.append((btt['start'], btt['tagend'], nbtag))

    seg = apply_edits(seg, edits)
    seg, nsvg = hide_svgs(seg)
    assert nsvg == 21, f'footer svgs: {nsvg}'
    # frame -> footer
    assert seg.startswith('<div')
    seg = '<footer' + seg[4:]
    assert seg.rstrip().endswith('</div>')
    seg = seg.rstrip()[:-len('</div>')] + '</footer>'
    return seg


# ---------------------------------------------------------------- apply
FRAME_FILES = {'index.html': 'index.html', 'contact.html': 'contact.html'}
OTHER_FILES = {'experience.html': 'experience.html', 'project.html': 'project.html',
               'mobile-pos.html': 'project.html', 'dbank-pro.html': 'project.html',
               'upcademy.html': 'project.html', 'waste4change.html': 'project.html',
               'niagahoster.html': 'project.html', 'warunk-upnormal.html': 'project.html'}


def insert_style(doc):
    elems = parse(doc)
    f12 = by_name(elems, 'Frame 12')
    return doc[:f12['start']] + STYLE_BLOCK + doc[f12['start']:]


def replace_frame(doc, own):
    elems = parse(doc)
    frame = next(el for el in elems if el['attrs'].get('id') == 'contact')
    return doc[:frame['start']] + build_footer_frame(own, own) + doc[frame['end']:]


def graft_frame(doc, own):
    elems = parse(doc)
    mac = by_name(elems, 'Macbook 14"')
    ex = by_name(elems, 'explore')
    clock = next(el for el in elems if 'data-live-clock' in el['attrs'])
    assert mac['start'] <= ex['start'] and clock['end'] <= mac['end']
    frame = build_footer_frame(own, own)
    return doc[:ex['start']] + doc[clock['end']:mac['end']] + '\n' + frame + doc[mac['end']:]


def verify(fname, doc, own):
    elems = parse(doc)
    f12 = by_name(elems, 'Frame 12')
    assert f12['tag'] == 'header', f'{fname}: Frame 12 tag {f12["tag"]}'
    navs = [el for el in elems if el['tag'] == 'nav']
    labels = sorted(el['attrs'].get('aria-label', '') for el in navs)
    assert 'Main' in labels, f'{fname}: navs {labels}'
    frame = next(el for el in elems if el['attrs'].get('id') == 'contact')
    assert frame['tag'] == 'footer', f'{fname}: contact tag {frame["tag"]}'
    clocks = [el for el in elems if 'data-live-clock' in el['attrs']]
    assert len(clocks) == 1 and clocks[0]['tag'] == 'time', f'{fname}: clock'
    h = by_name(elems, 'Have a question or just want to say hi?')
    assert h['tag'] == 'h2', f'{fname}: headline tag {h["tag"]}'
    hdr_aria = doc[f12['start']:f12['end']].count('aria-current')
    exp_hdr = 0 if fname == 'index.html' else 1
    assert hdr_aria == exp_hdr, f'{fname}: header aria-current {hdr_aria}'
    ftr_aria = doc[frame['start']:frame['end']].count('aria-current')
    assert ftr_aria == 1, f'{fname}: footer aria-current {ftr_aria}'
    assert doc.count('contact-blue-sticker') >= 1, f'{fname}: sticker'
    assert doc.count('<svg aria-hidden') >= 28, f'{fname}: hidden svgs {doc.count("<svg aria-hidden")}'
    assert doc.count('kp-explore-label') == 2, f'{fname}: explore label refs'
    assert doc.count(STYLE_BLOCK) == 1, f'{fname}: style block'
    # balanced tags
    from html.parser import HTMLParser as HP
    stack = []

    class V(HP):
        def handle_starttag(self, t, a):
            if t not in VOID:
                stack.append(t)

        def handle_startendtag(self, t, a):
            pass

        def handle_endtag(self, t):
            if t in VOID:
                return
            assert stack and stack[-1] == t, f'{fname}: unbalanced at {t}, top {stack[-3:]}'
            stack.pop()

    v = V(convert_charrefs=False)
    v.feed(doc)
    assert not stack, f'{fname}: unclosed {stack}'
    print(f'{fname}: OK ({len(doc)} bytes)')


def main():
    for fname, own in {**FRAME_FILES, **OTHER_FILES}.items():
        doc = open(REPO + fname, encoding='utf-8').read()
        doc = transform_header(doc)
        doc = insert_style(doc)
        doc = replace_frame(doc, own) if fname in FRAME_FILES else graft_frame(doc, own)
        verify(fname, doc, own)
        open(REPO + fname, 'w', encoding='utf-8').write(doc)
    print('ALL DONE')


if __name__ == '__main__':
    main()

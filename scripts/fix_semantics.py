#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Semantic fixes (audit points 1-6) + navbar separation for Kinanti-Portfolio.

Per page:
- move the <header> (with its style block) out of the page frame so it becomes
  a direct child of the outer wrapper, a section of its own (it is
  position:fixed, so the move is layout-neutral)
- upgrade the style block: visually-hidden utility + restore the fluid side
  padding for the wrapper's <main> and <footer> children (the old responsive
  rule targeted divs only, so the footer silently lost its designed inset in
  the previous rebuild when it stopped being a div)
- the page frame (Macbook) becomes <main>; on contact.html it holds only the
  header, so the empty frame is removed instead
- h1: convert the visible page title on experience/project, convert fs-40
  section titles on index/project to h2, add a visually hidden h1 on index
  (hero is artwork) and contact
- meaningful <img> alts on index/project (project covers, screenshots,
  avatars); the tool logo strip stays decorative
- hide every remaining decorative <svg> from assistive tech
- lang="id" on the four Indonesian case studies
- a meta description per page
"""
import re
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
PAGES = ['index.html', 'experience.html', 'project.html', 'contact.html',
         'mobile-pos.html', 'dbank-pro.html', 'upcademy.html', 'waste4change.html',
         'niagahoster.html', 'warunk-upnormal.html']
ID_PAGES = {'dbank-pro.html', 'upcademy.html', 'waste4change.html', 'niagahoster.html'}
VOID = {'meta', 'link', 'img', 'br', 'hr', 'input', 'source'}

NEW_STYLE = ('\n<style>\n'
 '.kp-visually-hidden { position: absolute !important; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }\n'
 '[data-pencil-name="Frame 9478"] > main, [data-pencil-name="Frame 9478"] > footer { padding-left: clamp(20px, 6.42vw, 97px) !important; padding-right: clamp(20px, 6.42vw, 97px) !important; }\n'
 '[data-pencil-name="Frame 12"] a:focus-visible, #contact a:focus-visible { outline: 3px solid #2185e3; outline-offset: 3px; border-radius: 6px; }\n'
 '</style>\n')

DESC = {
 'index.html': 'Portfolio of Kinanti Ayudya Putri Rahardiani, a UI/UX designer crafting web and mobile experiences, from research and design systems to chatbot and product design.',
 'experience.html': "Kinanti's experience as a UI/UX designer and intern, across product teams and design projects.",
 'project.html': 'Selected UI/UX projects by Kinanti Ayudya Putri Rahardiani: Mobile POS research, DBank Pro redesign, Waste4Change, Niagahoster checkout, UpCademy, and more.',
 'contact.html': 'Contact Kinanti Ayudya Putri Rahardiani for UI/UX design work and collaboration.',
 'mobile-pos.html': 'UX research case study evaluating Mobile POS usage by store cashiers for an outdoor retail company: field observation, think-aloud testing, and interviews.',
 'dbank-pro.html': 'Studi kasus redesign fitur Top Up dan Info Kartu Kredit DBank Pro dari Bank Danamon, dengan skor usability testing rata-rata 8,6 dari 10.',
 'upcademy.html': 'Studi kasus UX UpCademy, platform edukasi online: desain flow pendaftaran, transaksi kelas, dan pembelajaran dengan metode Design Thinking.',
 'waste4change.html': 'Studi kasus redesign layanan Send Your Waste dari Waste4Change: form pengiriman, pembayaran, dan redeem points untuk desktop dan mobile.',
 'niagahoster.html': 'Redesign halaman checkout Niagahoster agar pengguna lebih cepat dan percaya diri memilih paket hosting, teruji dengan nilai rata-rata 8,5 dari 10.',
 'warunk-upnormal.html': 'Case study on bringing customers back to Warunk Upnormal: desk research, interviews, and three solution tracks, from feedback rewards to self-service Indomie.',
}

ALTS = {
 'assets/avatar-1.webp': 'Kinanti Ayudya Putri Rahardiani',
 'assets/avatar-2.webp': 'Kinanti Ayudya Putri Rahardiani',
 'assets/project-mpos.png': 'Mobile POS Usage Evaluation project cover',
 'assets/project-warunk-upnormal.webp': 'Warunk Upnormal project cover',
 'assets/project-dbank-pro.webp': 'DBank Pro redesign project cover',
 'assets/project-waste4change.webp': 'Waste4Change Send Your Waste project cover',
 'assets/project-niagahoster.webp': 'Niagahoster checkout redesign project cover',
 'assets/project-upcademy.webp': 'UpCademy project cover',
 'assets/superindo-1.webp': 'Super Indo Recipe Chatbot design 1',
 'assets/superindo-2.webp': 'Super Indo Recipe Chatbot design 2',
 'assets/superindo-3.png': 'Super Indo Recipe Chatbot design 3',
 'assets/ayosehat-1.webp': 'AyoSehat Chatbot design 1',
 'assets/ayosehat-2.webp': 'AyoSehat Chatbot design 2',
}

H1_CONVERT = {'experience.html': 'Experience', 'project.html': 'UI/UX Project'}
H2_CONVERT = {
 'index.html': ['Experience', 'UI/UX Project', 'Chatbot development', 'social media design', 'how i design', 'tools'],
 'project.html': ['Chatbot development', 'social media design', 'how i design', 'tools'],
}
HIDDEN_H1 = {'index.html': 'Kinanti — UI/UX Designer', 'contact.html': 'Contact — Kinanti'}


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
                    'tagend': s + len(raw), 'end': None, 'close_start': None,
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
                    self.stack[i]['close_start'] = e
                    self.stack[i]['end'] = gt + 1
                    if i > 0:
                        self.stack[i - 1]['own'] += self.stack[i]['own']
                    del self.stack[i:]
                    break

    p = P()
    p.feed(src)
    return p.elems


def is_desc(el, anc):
    p = el['parent']
    while p is not None:
        if p is anc:
            return True
        p = p['parent']
    return False


def fs_of(el):
    m = re.search(r'font-size: (\d+)px', el['attrs'].get('style', ''))
    return int(m.group(1)) if m else None


def text_of(el):
    return re.sub(r'\s+', ' ', el['own']).strip()


for fname in PAGES:
    path = REPO + fname
    src = open(path, encoding='utf-8').read()
    if 'kp-visually-hidden' in src:
        print('skip (already fixed)', fname)
        continue

    # --- A: cut the header chunk (style block + header) ---------------------
    els = parse(src)
    header = next(e for e in els if e['tag'] == 'header')
    style_start = src.rfind('<style>', 0, header['start'])
    assert style_start != -1 and 'focus-visible' in src[style_start:header['start']]
    new_chunk = NEW_STYLE + src[header['start']:header['end']]
    src = src[:style_start] + src[header['end']:]

    # --- B: insert the chunk right after the outer wrapper opens -----------
    els = parse(src)
    outer = next(e for e in els if e['attrs'].get('data-pencil-name') == 'Frame 9478')
    src = src[:outer['tagend']] + new_chunk + src[outer['tagend']:]

    # --- C: frame -> <main>, or drop the empty frame on contact ------------
    els = parse(src)
    mac = next((e for e in els if e['attrs'].get('data-pencil-name') == 'Macbook 14"'), None)
    if mac is None:
        assert fname == 'contact.html', f'{fname}: page frame not found'
        # contact.html has no page frame: its content is the footer section
        # itself, so there is nothing to convert or remove here.
        pass
    elif fname == 'contact.html':
        inner = re.sub(r'<[^>]+>', '', src[mac['tagend']:mac['close_start']]).strip()
        assert inner == '', f'contact frame not empty: {inner[:80]!r}'
        src = src[:mac['start']] + src[mac['end']:]
    else:
        src = (src[:mac['start']]
               + '<main' + src[mac['start'] + 4:mac['tagend']]
               + src[mac['tagend']:mac['close_start']]
               + '</main>'
               + src[mac['end']:])

    # --- D: heading conversions + hidden h1 ---------------------------------
    els = parse(src)
    main_el = next((e for e in els if e['tag'] == 'main'), None)
    edits = []
    wanted = {}
    if fname in H1_CONVERT:
        wanted[H1_CONVERT[fname]] = 'h1'
    for t in H2_CONVERT.get(fname, []):
        wanted[t] = 'h2'
    found = {t: 0 for t in wanted}
    for e in els:
        if e['tag'] != 'div' or fs_of(e) != 40:
            continue
        if main_el is not None and not is_desc(e, main_el):
            continue
        t = text_of(e)
        if t not in wanted:
            continue
        found[t] += 1
        target = wanted[t]
        seg = src[e['start']:e['tagend']]
        if 'margin:' not in seg:
            seg = seg[:-1].rstrip() + '; margin: 0">'
        edits.append((e['start'], e['tagend'], '<' + target + seg[4:]))
        edits.append((e['close_start'], e['end'], '</' + target + '>'))
    for t, c in found.items():
        assert c == 1, f'{fname}: heading {t!r} found {c} times'
    if fname in HIDDEN_H1:
        if main_el is not None:
            at = main_el['tagend']
        else:
            hdr = next(e for e in els if e['tag'] == 'header')
            at = hdr['end']
        edits.append((at, at, '\n<h1 class="kp-visually-hidden">' + HIDDEN_H1[fname] + '</h1>'))
    for s, e_, rep in sorted(edits, key=lambda x: x[0], reverse=True):
        src = src[:s] + rep + src[e_:]

    # --- F: image alts --------------------------------------------------------
    def alt_sub(m):
        tag = m.group(0)
        sm = re.search(r'src="([^"]+)"', tag)
        if sm and sm.group(1) in ALTS:
            return tag.replace('alt=""', 'alt="' + ALTS[sm.group(1)] + '"', 1)
        return tag
    src = re.sub(r'<img\b[^>]*>', alt_sub, src)

    # --- G: hide remaining decorative svgs ------------------------------------
    src = re.sub(r'<svg(?![^>]*aria-hidden)', '<svg aria-hidden="true" focusable="false"', src)

    # --- H: language ------------------------------------------------------------
    if fname in ID_PAGES:
        assert '<html lang="en">' in src
        src = src.replace('<html lang="en">', '<html lang="id">', 1)

    # --- I: meta description ------------------------------------------------------
    assert 'name="description"' not in src
    src = re.sub(r'(</title>)', r'\1\n<meta name="description" content="' + DESC[fname] + '">', src, count=1)

    open(path, 'w', encoding='utf-8').write(src)
    print('fixed', fname)

print('ALL FIXED')

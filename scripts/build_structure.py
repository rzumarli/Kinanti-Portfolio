#!/usr/bin/env python3
"""Regenerate structure.html from index.html with the v2 inspection layer.

v2 (2026-11-27) replaces the v1 dense-only overlay with:
  - a collapsible element tree panel on the left (tag + Pencil name),
  - click a tree row (or, in inspect mode, click the element itself) to
    highlight ONLY that element with its dimension lines,
  - an info panel: tag, name, size, padding, margin, position, child count,
  - the v1 overview mode (all outlines, labels, dimension lines) stays
    available from the toolbar.

Run from anywhere:  python3 scripts/build_structure.py
Never edit structure.html by hand.
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LAYER = r"""
<style>
#sv-panel{position:fixed;top:0;left:0;bottom:0;width:330px;z-index:99990;background:#fff;border-right:2px solid #363636;display:flex;flex-direction:column;font-family:"DM Sans",system-ui,sans-serif;color:#363636;transform:translateX(0);transition:transform .18s ease}
#sv-panel.sv-hidden{transform:translateX(-332px)}
#sv-panel header{padding:12px 14px 10px;border-bottom:2px solid #363636}
#sv-panel h2{font-family:Silkscreen,monospace;font-size:16px;margin:0 0 4px;font-weight:700}
#sv-panel p{font-size:12px;line-height:1.45;margin:0;color:#6b655c}
#sv-panel a{color:#2185e3}
#sv-tree{flex:1;overflow:auto;padding:8px 6px;font-size:12.5px;line-height:1.35}
#sv-tree ul{list-style:none;margin:0;padding-left:14px}
#sv-tree>ul{padding-left:2px}
#sv-tree li{white-space:nowrap}
.sv-row{display:flex;align-items:center;gap:4px;padding:2px 6px;border-radius:6px;cursor:pointer}
.sv-row:hover{background:#f3efe9}
.sv-row.sv-sel{background:#ffe1d6;outline:2px solid #f85c36}
.sv-tw{width:14px;height:14px;flex:0 0 14px;border:1.5px solid #363636;border-radius:4px;background:#fff;font-size:10px;line-height:1;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0}
.sv-tw.sv-leaf{visibility:hidden}
.sv-tag{font-family:ui-monospace,Menlo,monospace;font-weight:700;color:#2185e3}
.sv-name{color:#363636;overflow:hidden;text-overflow:ellipsis}
.sv-name.sv-gen{color:#9a917f;font-style:italic}
#sv-info{border-top:2px solid #363636;padding:10px 14px;font-size:12.5px;min-height:118px}
#sv-info h3{font-family:Silkscreen,monospace;font-size:13px;margin:0 0 6px;font-weight:700}
#sv-info table{border-collapse:collapse}
#sv-info td{padding:1.5px 10px 1.5px 0;vertical-align:top}
#sv-info td:first-child{color:#8a8178;font-family:ui-monospace,Menlo,monospace;font-size:11.5px}
#sv-info td:last-child{font-family:ui-monospace,Menlo,monospace}
#sv-bar{position:fixed;left:344px;bottom:14px;z-index:99991;display:flex;gap:8px;flex-wrap:wrap;transition:left .18s ease}
#sv-bar.sv-shift{left:14px}
#sv-bar button{font-family:Silkscreen,monospace;font-size:12px;font-weight:700;background:#fff;color:#363636;border:2px solid #363636;border-radius:999px;padding:7px 14px;cursor:pointer}
#sv-bar button[aria-pressed="true"]{background:#363636;color:#fff}
.sv-ol{outline:2px solid rgba(33,133,227,.75)!important;outline-offset:-2px}
.sv-ol-main{outline-color:rgba(22,163,74,.9)!important}
.sv-ol-header{outline-color:rgba(248,92,54,.95)!important}
.sv-ol-footer{outline-color:rgba(227,6,19,.9)!important}
.sv-ol-nav{outline-color:rgba(147,51,234,.9)!important}
.sv-ol-sec{outline-color:rgba(13,148,136,.85)!important}
.sv-ol-head{outline:2px dashed rgba(254,127,196,.95)!important}
.sv-ol-a{outline:2px dotted rgba(248,92,54,.95)!important}
.sv-ol-img{outline:2px dashed rgba(139,92,246,.9)!important}
.sv-ol-list{outline:2px dotted rgba(146,64,14,.9)!important}
#sv-overlay{position:absolute;top:0;left:0;width:100%;height:0;z-index:99980;pointer-events:none}
.sv-lab{position:absolute;font-family:ui-monospace,Menlo,monospace;font-size:10px;line-height:1.3;background:#363636;color:#fff;padding:1px 5px;border-radius:4px;white-space:nowrap;transform:translateY(-100%)}
.sv-dim{position:absolute;background:#e30613}
.sv-dim span{position:absolute;font-family:ui-monospace,Menlo,monospace;font-size:10px;color:#e30613;background:rgba(255,255,255,.85);padding:0 3px;white-space:nowrap}
.sv-hl{position:absolute;border:3px solid #e30613;background:rgba(227,6,19,.08);box-sizing:border-box}
@media (max-width:760px){#sv-panel{width:86vw}#sv-bar{left:auto;right:10px;bottom:10px}}
</style>
<aside id="sv-panel" aria-label="Panel struktur elemen">
  <header>
    <h2>Struktur halaman</h2>
    <p>Klik nama frame untuk menyorot satu elemen saja. <a href="index.html">Kembali ke Home</a></p>
  </header>
  <nav id="sv-tree" aria-label="Pohon elemen"></nav>
  <section id="sv-info" aria-label="Info elemen terpilih"><h3>Belum ada elemen dipilih</h3><p style="margin:0;color:#6b655c">Pilih elemen dari pohon, atau nyalakan mode Inspeksi lalu klik elemen di halaman.</p></section>
</aside>
<div id="sv-bar" role="group" aria-label="Kontrol struktur">
  <button id="sv-btn-panel" aria-pressed="true">Panel</button>
  <button id="sv-btn-stroke" aria-pressed="false">Stroke semua</button>
  <button id="sv-btn-label" aria-pressed="false">Label</button>
  <button id="sv-btn-dims" aria-pressed="false">Ukuran semua</button>
  <button id="sv-btn-inspect" aria-pressed="false">Inspeksi</button>
</div>
<div id="sv-overlay"></div>
<script>
(function(){
  "use strict";
  var SKIP = {SCRIPT:1, STYLE:1, LINK:1, META:1, NOSCRIPT:1, BR:1, WBR:1};
  var panel = document.getElementById('sv-panel'),
      treeBox = document.getElementById('sv-tree'),
      info = document.getElementById('sv-info'),
      overlay = document.getElementById('sv-overlay'),
      bar = document.getElementById('sv-bar');
  var state = {stroke:false, label:false, dims:false, inspect:false, selected:null};
  var counters = {}, nodes = new Map(), selectedRow = null;

  function elName(el){
    var n = el.getAttribute('data-pencil-name');
    if (n) return {t:n, gen:false};
    if (el.id) return {t:'#'+el.id, gen:false};
    if (el.classList && el.classList.length) return {t:'.'+el.classList[0], gen:false};
    var tag = el.tagName.toLowerCase();
    counters[tag] = (counters[tag]||0)+1;
    return {t:tag+' '+counters[tag], gen:true};
  }
  function isOurs(el){
    return el.closest && (el.closest('#sv-panel') || el.closest('#sv-bar') || el.closest('#sv-overlay'));
  }
  function buildTree(rootEl, parentUl, depth){
    var kids = rootEl.children;
    for (var i=0;i<kids.length;i++){
      var el = kids[i];
      if (SKIP[el.tagName] || isOurs(el)) continue;
      var li = document.createElement('li');
      var row = document.createElement('div');
      row.className = 'sv-row';
      var nm = elName(el);
      var hasKids = el.children.length && el.tagName !== 'SVG';
      var tw = document.createElement('button');
      tw.className = 'sv-tw' + (hasKids ? '' : ' sv-leaf');
      tw.textContent = depth >= 1 ? '+' : '−';
      tw.setAttribute('aria-label','Buka atau tutup cabang');
      row.appendChild(tw);
      var lab = document.createElement('span');
      lab.innerHTML = '<span class="sv-tag"></span> <span class="sv-name"></span>';
      lab.querySelector('.sv-tag').textContent = el.tagName.toLowerCase();
      var nameSpan = lab.querySelector('.sv-name');
      nameSpan.textContent = nm.t;
      if (nm.gen) nameSpan.classList.add('sv-gen');
      row.appendChild(lab);
      li.appendChild(row);
      var ul = null;
      if (hasKids){
        ul = document.createElement('ul');
        if (depth >= 1) ul.style.display = 'none';
        li.appendChild(ul);
        buildTree(el, ul, depth+1);
      }
      nodes.set(el, {row:row, li:li});
      (function(el, ul, tw){
        tw.addEventListener('click', function(ev){
          ev.stopPropagation();
          if (!ul) return;
          var open = ul.style.display !== 'none';
          ul.style.display = open ? 'none' : '';
          tw.textContent = open ? '+' : '−';
        });
        row.addEventListener('click', function(){ select(el, true); });
      })(el, ul, tw);
      parentUl.appendChild(li);
    }
  }
  var rootUl = document.createElement('ul');
  treeBox.appendChild(rootUl);
  buildTree(document.body, rootUl, 0);

  function rectOf(el){
    var r = el.getBoundingClientRect();
    return {x:r.left + window.scrollX, y:r.top + window.scrollY, w:r.width, h:r.height};
  }
  function clearOverlay(){ overlay.innerHTML=''; }
  function dimLines(el, withBox){
    var r = rectOf(el);
    if (r.w < 2 || r.h < 2) return;
    if (withBox){
      var box = document.createElement('div');
      box.className = 'sv-hl';
      box.style.left = r.x+'px'; box.style.top = r.y+'px';
      box.style.width = r.w+'px'; box.style.height = r.h+'px';
      overlay.appendChild(box);
    }
    var dh = document.createElement('div');
    dh.className = 'sv-dim';
    dh.style.left = r.x+'px'; dh.style.top = (r.y+3)+'px';
    dh.style.width = r.w+'px'; dh.style.height = '1px';
    dh.innerHTML = '<span></span>';
    var s = dh.querySelector('span');
    s.textContent = Math.round(r.w)+'px';
    s.style.left = '50%'; s.style.top = '-6px'; s.style.transform = 'translateX(-50%)';
    overlay.appendChild(dh);
    var dv = document.createElement('div');
    dv.className = 'sv-dim';
    dv.style.left = (r.x+3)+'px'; dv.style.top = r.y+'px';
    dv.style.width = '1px'; dv.style.height = r.h+'px';
    dv.innerHTML = '<span></span>';
    var s2 = dv.querySelector('span');
    s2.textContent = Math.round(r.h)+'px';
    s2.style.top = '50%'; s2.style.left = '2px'; s2.style.transform = 'rotate(-90deg) translateX(50%)';
    s2.style.transformOrigin = 'left center';
    overlay.appendChild(dv);
  }
  function short4(cs, a, b, c, d){
    var v = [cs[a], cs[b], cs[c], cs[d]];
    if (v[0]===v[1] && v[1]===v[2] && v[2]===v[3]) return v[0];
    if (v[0]===v[2] && v[1]===v[3]) return v[0]+' '+v[1];
    return v.join(' ');
  }
  function fillInfo(el){
    var cs = getComputedStyle(el);
    var r = rectOf(el);
    var nm = elName(el).t;
    var rows = [
      ['tag', el.tagName.toLowerCase()],
      ['nama', nm],
      ['ukuran', Math.round(r.w)+' × '+Math.round(r.h)+' px'],
      ['padding', short4(cs,'paddingTop','paddingRight','paddingBottom','paddingLeft')],
      ['margin', short4(cs,'marginTop','marginRight','marginBottom','marginLeft')],
      ['position', cs.position],
      ['anak', String(el.children.length)]
    ];
    var h = '<h3>Elemen terpilih</h3><table>';
    rows.forEach(function(p){
      var tr = document.createElement('tr');
      var t1 = document.createElement('td'); t1.textContent = p[0];
      var t2 = document.createElement('td'); t2.textContent = p[1];
      tr.appendChild(t1); tr.appendChild(t2);
      h += tr.outerHTML;
    });
    info.innerHTML = h + '</table>';
  }
  function select(el, scrollTree){
    state.selected = el;
    if (selectedRow) selectedRow.classList.remove('sv-sel');
    var rec = nodes.get(el);
    if (rec){
      selectedRow = rec.row;
      rec.row.classList.add('sv-sel');
      var li = rec.li.parentElement;
      while (li && li !== treeBox){
        if (li.tagName === 'UL') li.style.display = '';
        li = li.parentElement;
      }
      if (scrollTree) rec.row.scrollIntoView({block:'nearest'});
    }
    clearOverlay();
    dimLines(el, true);
    fillInfo(el);
  }
  function outlineClass(el){
    var t = el.tagName.toLowerCase();
    if (t === 'main') return 'sv-ol sv-ol-main';
    if (t === 'header') return 'sv-ol sv-ol-header';
    if (t === 'footer') return 'sv-ol sv-ol-footer';
    if (t === 'nav') return 'sv-ol sv-ol-nav';
    if (t === 'section' || t === 'article') return 'sv-ol sv-ol-sec';
    if (/^h[1-6]$/.test(t)) return 'sv-ol sv-ol-head';
    if (t === 'a') return 'sv-ol sv-ol-a';
    if (t === 'img' || t === 'svg') return 'sv-ol sv-ol-img';
    if (t === 'ul' || t === 'li') return 'sv-ol sv-ol-list';
    return 'sv-ol';
  }
  function allElements(){
    var out = [];
    var walk = function(el){
      var kids = el.children;
      for (var i=0;i<kids.length;i++){
        var k = kids[i];
        if (SKIP[k.tagName] || isOurs(k)) continue;
        out.push(k);
        if (k.tagName !== 'SVG') walk(k);
      }
    };
    walk(document.body);
    return out;
  }
  function redrawOverview(){
    document.querySelectorAll('.sv-ol').forEach(function(e){
      e.classList.remove('sv-ol','sv-ol-main','sv-ol-header','sv-ol-footer','sv-ol-nav','sv-ol-sec','sv-ol-head','sv-ol-a','sv-ol-img','sv-ol-list');
    });
    clearOverlay();
    if (state.selected) dimLines(state.selected, true);
    if (!state.stroke && !state.label && !state.dims) return;
    var els = allElements();
    var labelled = 0;
    els.forEach(function(el){
      var r = rectOf(el);
      if (r.w < 2 || r.h < 2) return;
      if (state.stroke) el.classList.add.apply(el.classList, outlineClass(el).split(' '));
      if (state.dims && r.w >= 60 && r.h >= 24) dimLines(el, false);
      if (state.label && r.w >= 60 && r.h >= 24 && labelled < 300){
        labelled++;
        var lab = document.createElement('div');
        lab.className = 'sv-lab';
        lab.style.left = r.x+'px'; lab.style.top = r.y+'px';
        lab.textContent = el.tagName.toLowerCase()+' · '+elName(el).t;
        overlay.appendChild(lab);
      }
    });
  }
  var timer = null;
  function schedule(){ clearTimeout(timer); timer = setTimeout(redrawOverview, 120); }
  window.addEventListener('scroll', schedule, {passive:true});
  window.addEventListener('resize', schedule);

  function bindToggle(id, key, fn){
    var b = document.getElementById(id);
    b.addEventListener('click', function(){
      state[key] = !state[key];
      b.setAttribute('aria-pressed', String(state[key]));
      if (fn) fn();
      redrawOverview();
    });
  }
  bindToggle('sv-btn-stroke', 'stroke');
  bindToggle('sv-btn-label', 'label');
  bindToggle('sv-btn-dims', 'dims');
  bindToggle('sv-btn-inspect', 'inspect');
  document.getElementById('sv-btn-panel').addEventListener('click', function(){
    var hidden = panel.classList.toggle('sv-hidden');
    this.setAttribute('aria-pressed', String(!hidden));
    bar.classList.toggle('sv-shift', hidden);
  });
  document.addEventListener('click', function(ev){
    if (!state.inspect) return;
    if (isOurs(ev.target)) return;
    ev.preventDefault();
    ev.stopPropagation();
    select(ev.target, true);
  }, true);
  redrawOverview();
})();
</script>
"""

src = open(os.path.join(REPO, "index.html"), encoding="utf-8").read()
assert 'id="sv-panel"' not in src, "structure layer already present in index.html"
out = src.replace('<meta name="viewport"', '<meta name="robots" content="noindex" />\n    <meta name="viewport"', 1)
assert out != src, "viewport meta anchor not found"
assert out.count("</body>") == 1
out = out.replace("</body>", LAYER + "\n</body>", 1)
open(os.path.join(REPO, "structure.html"), "w", encoding="utf-8").write(out)
print("structure.html regenerated:", len(out), "bytes")

/* Burjoempa fan carousel (phones only, max-width 720px).
   The gallery tiles become a fanned deck: the active card stands
   upright at full size, its neighbours shrink to 86% and tilt
   15 degrees to each side, following the layout Rahmat exported.
   Swipe or drag to move, tap a side card to bring it forward.
   On wider screens the script does nothing and the normal
   gallery layout applies. */
(function () {
  var stage = document.querySelector('[data-pencil-name="Frame 8897"]');
  if (!stage) return;
  var slides = Array.prototype.slice.call(stage.children);
  if (slides.length < 2) return;

  var mq = window.matchMedia('(max-width: 720px)');
  var active = 0;
  var frac = 0; // live drag offset, in card steps
  var counter = null;
  var on = false;

  function render() {
    var w = stage.clientWidth || 345;
    slides.forEach(function (el, i) {
      var o = i - active + frac;
      var ao = Math.abs(o);
      var x = o * w * 0.574;
      var s = 1 - Math.min(ao, 1) * 0.14;
      var r = Math.max(-1, Math.min(1, o)) * 15;
      var y = Math.min(ao, 1) * 12;
      var op = ao <= 1 ? 1 : Math.max(0, 1 - (ao - 1));
      var t =
        'translate(-50%, 0px) translateX(' + x.toFixed(1) + 'px)' +
        ' translateY(' + y.toFixed(1) + 'px) scale(' + s.toFixed(3) + ')' +
        ' rotate(' + r.toFixed(2) + 'deg)';
      el.style.setProperty('transform', t, 'important');
      el.style.opacity = op.toFixed(3);
      el.style.zIndex = String(100 - Math.round(ao * 10) + (o < 0 ? 1 : 0));
      el.style.pointerEvents = ao > 1.6 ? 'none' : 'auto';
    });
    if (counter) counter.textContent = active + 1 + ' / ' + slides.length;
  }

  function go(i) {
    active = Math.max(0, Math.min(slides.length - 1, i));
    frac = 0;
    render();
  }

  /* --- drag / swipe --- */
  var dragging = false, startX = 0, moved = 0, suppressClick = false;

  stage.addEventListener('pointerdown', function (e) {
    if (!on) return;
    dragging = true;
    moved = 0;
    startX = e.clientX;
    stage.classList.add('dragging');
    stage.setPointerCapture(e.pointerId);
  });

  stage.addEventListener('pointermove', function (e) {
    if (!dragging) return;
    var dx = e.clientX - startX;
    moved = Math.max(moved, Math.abs(dx));
    var f = dx / 240;
    // resistance past the first and last card
    if ((active === 0 && f > 0) || (active === slides.length - 1 && f < 0)) f *= 0.35;
    frac = f;
    render();
  });

  function endDrag() {
    if (!dragging) return;
    dragging = false;
    stage.classList.remove('dragging');
    if (frac < -0.22) active += 1;
    else if (frac > 0.22) active -= 1;
    if (moved > 8) {
      suppressClick = true;
      setTimeout(function () { suppressClick = false; }, 50);
    }
    go(active);
  }
  stage.addEventListener('pointerup', endDrag);
  stage.addEventListener('pointercancel', endDrag);

  slides.forEach(function (el, i) {
    el.addEventListener('click', function () {
      if (!on || suppressClick || i === active) return;
      go(i);
    });
  });

  stage.setAttribute('tabindex', '0');
  stage.addEventListener('keydown', function (e) {
    if (!on) return;
    if (e.key === 'ArrowRight') { go(active + 1); e.preventDefault(); }
    if (e.key === 'ArrowLeft') { go(active - 1); e.preventDefault(); }
  });

  window.addEventListener('resize', function () { if (on) render(); });

  /* --- activate only on phones --- */
  function activate() {
    if (on) return;
    on = true;
    stage.classList.add('carousel-on');
    counter = document.createElement('div');
    counter.className = 'burjo-counter';
    stage.insertAdjacentElement('afterend', counter);
    go(0);
  }

  function deactivate() {
    if (!on) return;
    on = false;
    stage.classList.remove('carousel-on');
    if (counter) { counter.remove(); counter = null; }
    slides.forEach(function (el) {
      el.style.removeProperty('transform');
      el.style.removeProperty('opacity');
      el.style.removeProperty('z-index');
      el.style.removeProperty('pointer-events');
    });
  }

  function sync() { mq.matches ? activate() : deactivate(); }
  if (mq.addEventListener) mq.addEventListener('change', sync);
  else if (mq.addListener) mq.addListener(sync);
  sync();
})();

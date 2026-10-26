/* The Two-Piece Edit — product page interactions (staging build)
   Plain ES5-compatible JS. No fetch(), no modules: works from file://. */

(function () {
  'use strict';

  var P = window.PRODUCT;
  if (!P) return;

  /* ---------- gallery ---------- */
  var mainImg = document.getElementById('mainImg');
  var thumbs = Array.prototype.slice.call(document.querySelectorAll('.thumb'));

  function setImage(src, alt) {
    if (!mainImg || !src || mainImg.getAttribute('src') === src) return;
    mainImg.setAttribute('src', src);
    if (alt) mainImg.setAttribute('alt', alt);
  }

  thumbs.forEach(function (t) {
    t.addEventListener('click', function () {
      thumbs.forEach(function (o) {
        o.classList.remove('is-active');
        o.setAttribute('aria-selected', 'false');
      });
      t.classList.add('is-active');
      t.setAttribute('aria-selected', 'true');
      setImage(t.getAttribute('data-src'), t.getAttribute('data-alt'));
    });
  });

  /* ---------- colourway + size availability ---------- */
  var colourWrap = document.getElementById('colours');
  var sizeWrap = document.getElementById('sizes');
  var availNote = document.getElementById('avail');
  var pickNote = document.getElementById('pick');
  var colourButtons = Array.prototype.slice.call(document.querySelectorAll('.chip-colour'));

  var state = { colour: 0, size: null };

  function current() { return P.colours[state.colour]; }

  function renderSizes() {
    if (!sizeWrap) return;
    var c = current();
    sizeWrap.innerHTML = '';

    P.sizes.forEach(function (s) {
      var ok = c.sizes.indexOf(s) > -1;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'chip chip-size' + (ok ? '' : ' is-unavailable');
      b.textContent = s;
      b.setAttribute('data-size', s);

      if (!ok) {
        b.setAttribute('aria-disabled', 'true');
        b.title = 'not available in this colour';
        b.addEventListener('click', function (e) { e.preventDefault(); });
      } else {
        b.setAttribute('aria-disabled', 'false');
        b.setAttribute('aria-pressed', state.size === s ? 'true' : 'false');
        b.addEventListener('click', function () { selectSize(s); });
      }
      sizeWrap.appendChild(b);
    });

    if (state.size && c.sizes.indexOf(state.size) === -1) state.size = null;

    if (availNote) {
      availNote.textContent = c.sizes.length + ' of ' + P.sizes.length +
        ' sizes available in ' + c.name;
    }
    renderPick();
  }

  function renderPick() {
    if (!pickNote) return;
    pickNote.textContent = current().name + (state.size ? ' · Size ' + state.size : ' · select a size');
  }

  function selectSize(s) {
    state.size = (state.size === s) ? null : s;
    Array.prototype.slice.call(sizeWrap.querySelectorAll('.chip-size')).forEach(function (b) {
      if (b.getAttribute('aria-disabled') === 'true') return;
      b.setAttribute('aria-pressed', b.getAttribute('data-size') === state.size ? 'true' : 'false');
    });
    renderPick();
  }

  function selectColour(i) {
    state.colour = i;
    colourButtons.forEach(function (b, n) {
      b.setAttribute('aria-pressed', n === i ? 'true' : 'false');
    });
    var c = current();
    if (c.img) {
      setImage(c.img, P.name + ' in ' + c.name);
      thumbs.forEach(function (t) {
        var active = t.getAttribute('data-src') === c.img;
        t.classList.toggle('is-active', active);
        t.setAttribute('aria-selected', active ? 'true' : 'false');
      });
    }
    renderSizes();
  }

  colourButtons.forEach(function (b, i) {
    b.addEventListener('click', function () { selectColour(i); });
  });

  renderSizes();
})();

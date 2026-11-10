/* Kinanti Portfolio: swipe indicators for the chatbot phone strips.
   Adds a dot row under each phone strip (Super Indo and AyoSehat).
   The active dot follows the scroll position; tapping a dot scrolls
   to that phone. The dots are styled only at phone widths (720px and
   below) in css/responsive.css; on desktop the row stays hidden. */
(function () {
  var strips = document.querySelectorAll(
    '[data-pencil-name="Frame 8849"] > [data-pencil-name="Frame 8857"], ' +
      '[data-pencil-name="Frame 8849"] > [data-pencil-name="Frame 8856"]'
  );

  strips.forEach(function (strip) {
    var phones = Array.prototype.slice.call(strip.children);
    if (phones.length < 2) return;

    var dots = document.createElement("div");
    dots.className = "phone-strip-dots";

    phones.forEach(function (phone, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Go to screen " + (i + 1));
      b.addEventListener("click", function () {
        var sr = strip.getBoundingClientRect();
        var pr = phone.getBoundingClientRect();
        strip.scrollTo({
          left: strip.scrollLeft + (pr.left - sr.left),
          behavior: "smooth",
        });
      });
      dots.appendChild(b);
    });

    strip.insertAdjacentElement("afterend", dots);
    var buttons = dots.children;

    function update() {
      var sr = strip.getBoundingClientRect();
      var best = 0;
      var bestDist = Infinity;
      phones.forEach(function (phone, i) {
        var d = Math.abs(phone.getBoundingClientRect().left - sr.left);
        if (d < bestDist) {
          bestDist = d;
          best = i;
        }
      });
      for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.toggle("is-active", i === best);
      }
    }

    var ticking = false;
    strip.addEventListener(
      "scroll",
      function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () {
          update();
          ticking = false;
        });
      },
      { passive: true }
    );

    update();
  });
})();

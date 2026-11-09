/* Kinanti Portfolio scripts, extracted from index.html */

/* --- script 1 --- */
      (function () {
        var DESIGN_WIDTH = 1512;

        function fitToViewport() {
          var viewportWidth = document.documentElement.clientWidth;
          var scale = Math.min(1, viewportWidth / DESIGN_WIDTH);
          document.documentElement.style.zoom = scale;

          // The page is scaled with CSS zoom, so 100vh no longer matches the
          // visible viewport. Convert the viewport height into design pixels.
          var viewportHeight = window.innerHeight / scale;
          document.documentElement.style.setProperty("--hero-vh", viewportHeight + "px");

          var hero = document.querySelector(".hero-section");
          if (!hero) return;

          var frame19 = hero.querySelector('[data-pencil-name="Frame 19"]');
          var actions = hero.querySelector('[data-pencil-name="Frame 26"]');
          if (!frame19 || !actions) return;

          // Shrink the decorative offset on shorter screens so the hero always
          // fills exactly one viewport instead of overflowing past it.
          var styles = getComputedStyle(hero);
          var fixedHeight =
            parseFloat(styles.paddingTop) +
            parseFloat(styles.paddingBottom) +
            parseFloat(styles.gap) +
            frame19.offsetHeight +
            actions.offsetHeight;
          var offset = Math.max(0, Math.min(411, viewportHeight - fixedHeight));
          document.documentElement.style.setProperty("--hero-offset", offset + "px");
        }

        fitToViewport();
        window.addEventListener("resize", fitToViewport);
        window.addEventListener("load", fitToViewport);
        if (document.fonts && document.fonts.ready) {
          document.fonts.ready.then(fitToViewport);
        }
      })();
    

/* --- script 2 --- */
      (function () {
        var container = document.querySelector(".experience-cards");
        if (!container) return;

        var cards = container.querySelectorAll(".exp-card, .exp-ornament");
        if (!cards.length) return;

        function dropCards() {
          cards.forEach(function (card) {
            card.classList.add("is-dropped");
          });
        }

        if (!("IntersectionObserver" in window)) {
          dropCards();
          return;
        }

        var observer = new IntersectionObserver(
          function (entries) {
            entries.forEach(function (entry) {
              if (entry.isIntersecting) {
                dropCards();
                observer.disconnect();
              }
            });
          },
          { threshold: 0.2, rootMargin: "0px 0px -8% 0px" }
        );

        observer.observe(container);
      })();
    

/* --- script 3 --- */
      (function () {
        var stack = document.querySelector(".project-stack");
        if (!stack) return;

        if (
          window.matchMedia &&
          window.matchMedia("(prefers-reduced-motion: reduce)").matches
        ) {
          return;
        }

        var items = Array.prototype.slice
          .call(stack.children)
          .filter(function (wrap) {
            return wrap.hasAttribute("data-pencil-name");
          })
          .map(function (wrap) {
            return {
              wrap: wrap,
              parts: Array.prototype.slice.call(wrap.children),
              pinTop: 0,
              lastY: null
            };
          });

        var ZONE = 150;
        var scale = 1;
        var ticking = false;

        function measure() {
          var zoomValue = parseFloat(
            getComputedStyle(document.documentElement).zoom
          );
          scale = isNaN(zoomValue) || !zoomValue ? 1 : zoomValue;

          items.forEach(function (item) {
            var top = parseFloat(getComputedStyle(item.wrap).top);
            item.pinTop = (isNaN(top) ? 0 : top) * scale;
          });
        }

        function setOffset(item, y) {
          y = Math.round(y * 100) / 100;
          if (item.lastY === y) return;
          item.lastY = y;
          item.parts.forEach(function (part) {
            part.style.translate = y ? "0 " + y + "px" : "";
          });
        }

        function update() {
          ticking = false;
          if (!stack.getClientRects().length) return;

          items.forEach(function (item) {
            var distance = item.wrap.getBoundingClientRect().top - item.pinTop;
            var range = ZONE * scale;
            var y = 0;

            if (distance > 0 && distance < range) {
              // Magnetic pull with no overshoot: the card starts easing in
              // at scroll speed, gets drawn toward its stop, then settles
              // softly without snapping back.
              var t = distance / range;
              var remaining = 1 - t;
              y = -distance * remaining * remaining;
            }

            setOffset(item, y);
          });
        }

        function schedule() {
          if (ticking) return;
          ticking = true;
          requestAnimationFrame(update);
        }

        measure();
        update();
        window.addEventListener("scroll", schedule, { passive: true });
        window.addEventListener("resize", function () {
          measure();
          schedule();
        });
      })();
    

/* --- script 4 --- */
      (function () {
        var group = document.querySelector(
          '[data-pencil-name="Frame 8849"] > [data-pencil-name="Frame 8857"]'
        );
        if (!group) return;

        var phones = group.querySelectorAll(".superindo-phone");
        if (!phones.length) return;

        var shown = false;
        var observer = null;

        function showPhones() {
          if (shown) return;
          shown = true;
          phones.forEach(function (phone) {
            phone.classList.add("is-in");
          });
          if (observer) observer.disconnect();
          window.removeEventListener("scroll", check);
          window.removeEventListener("resize", check);
        }

        function check() {
          var rect = group.getBoundingClientRect();
          if (rect.top < window.innerHeight * 0.9 && rect.bottom > 0) {
            showPhones();
          }
        }

        if ("IntersectionObserver" in window) {
          observer = new IntersectionObserver(
            function (entries) {
              entries.forEach(function (entry) {
                if (entry.isIntersecting) showPhones();
              });
            },
            { threshold: 0.2, rootMargin: "0px 0px -8% 0px" }
          );
          observer.observe(group);
        }

        window.addEventListener("scroll", check, { passive: true });
        window.addEventListener("resize", check);
        check();
      })();
    

/* --- script 5 --- */
      (function () {
        var group = document.querySelector(
          '[data-pencil-name="Frame 8849"] > [data-pencil-name="Frame 8856"]'
        );
        if (!group) return;

        var phones = group.querySelectorAll(".ayosehat-phone");
        if (!phones.length) return;

        var shown = false;
        var observer = null;

        function showPhones() {
          if (shown) return;
          shown = true;
          phones.forEach(function (phone) {
            phone.classList.add("is-in");
          });
          if (observer) observer.disconnect();
          window.removeEventListener("scroll", check);
          window.removeEventListener("resize", check);
        }

        function check() {
          var rect = group.getBoundingClientRect();
          if (rect.top < window.innerHeight * 0.9 && rect.bottom > 0) {
            showPhones();
          }
        }

        if ("IntersectionObserver" in window) {
          observer = new IntersectionObserver(
            function (entries) {
              entries.forEach(function (entry) {
                if (entry.isIntersecting) showPhones();
              });
            },
            { threshold: 0.2, rootMargin: "0px 0px -8% 0px" }
          );
          observer.observe(group);
        }

        window.addEventListener("scroll", check, { passive: true });
        window.addEventListener("resize", check);
        check();
      })();
    

/* --- script 6 --- */
      (function () {
        var section = document.querySelector(".how-section");
        if (!section) return;

        var shown = false;
        var observer = null;

        function animateSection() {
          if (shown) return;
          shown = true;
          section.classList.add("is-animated");
          if (observer) observer.disconnect();
          window.removeEventListener("scroll", check);
          window.removeEventListener("resize", check);
        }

        function check() {
          var rect = section.getBoundingClientRect();
          if (rect.top < window.innerHeight * 0.9 && rect.bottom > 0) {
            animateSection();
          }
        }

        if ("IntersectionObserver" in window) {
          observer = new IntersectionObserver(
            function (entries) {
              entries.forEach(function (entry) {
                if (entry.isIntersecting) animateSection();
              });
            },
            { threshold: 0.2, rootMargin: "0px 0px -8% 0px" }
          );
          observer.observe(section);
        }

        window.addEventListener("scroll", check, { passive: true });
        window.addEventListener("resize", check);
        check();
      })();
    

/* --- script 7 --- */
      (function () {
        var card = document.querySelector('#contact [data-pencil-name="brand"]');
        if (!card) return;

        var targets = [
          card,
          document.querySelector("#contact .contact-blue-sticker"),
        ].filter(Boolean);

        function playAlert() {
          targets.forEach(function (element) {
            element.classList.remove("is-alerting");
            void element.offsetWidth;
            element.classList.add("is-alerting");
          });
        }

        function isCardVisible() {
          var rect = card.getBoundingClientRect();
          return rect.top < window.innerHeight * 0.9 && rect.bottom > 0;
        }

        function alertWhenVisible() {
          if (isCardVisible()) {
            playAlert();
            return;
          }

          var onScroll = function () {
            if (!isCardVisible()) return;
            window.removeEventListener("scroll", onScroll);
            playAlert();
          };

          window.addEventListener("scroll", onScroll, { passive: true });
          window.setTimeout(function () {
            window.removeEventListener("scroll", onScroll);
          }, 2500);
        }

        targets.forEach(function (element) {
          element.addEventListener("animationend", function () {
            element.classList.remove("is-alerting");
          });
        });

        document.addEventListener("click", function (event) {
          var link = event.target.closest('a[href="#contact"]');
          if (!link) return;
          alertWhenVisible();
        });
      })();
    

/* --- script 8 --- */
      (function () {
        var clock = document.querySelector("[data-live-clock]");
        if (!clock) return;

        var formatter = null;
        try {
          formatter = new Intl.DateTimeFormat("en-GB", {
            timeZone: "Asia/Jakarta",
            hour: "2-digit",
            minute: "2-digit",
            hourCycle: "h23",
          });
        } catch (error) {
          formatter = null;
        }

        function updateClock() {
          var now = new Date();
          var hours;
          var minutes;

          if (formatter) {
            var parts = formatter.formatToParts(now);
            parts.forEach(function (part) {
              if (part.type === "hour") hours = part.value;
              if (part.type === "minute") minutes = part.value;
            });
          }

          if (hours === undefined || minutes === undefined) {
            var utc = now.getTime() + now.getTimezoneOffset() * 60000;
            var jakarta = new Date(utc + 7 * 3600000);
            hours = String(jakarta.getUTCHours()).padStart(2, "0");
            minutes = String(jakarta.getUTCMinutes()).padStart(2, "0");
          }

          clock.textContent = hours + "." + minutes + " GMT+7";
        }

        updateClock();
        window.setInterval(updateClock, 1000);
      })();
    

/* --- script 9 --- */
      (function () {
        var nav = document.querySelector('[data-pencil-name="Frame 12"]');
        if (!nav) return;

        function updateNavPadding() {
          var scrolled = window.scrollY > 8;
          nav.classList.toggle("is-stuck", scrolled);
        }

        window.addEventListener("scroll", updateNavPadding, { passive: true });
        updateNavPadding();
      })();
    

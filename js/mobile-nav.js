/* Mobile navigation: adds a hamburger button to the fixed top bar.
   On small screens the link row (Frame 11) is hidden until the
   button expands it. Styling lives in css/responsive.css. */
(function () {
  var bar = document.querySelector('[data-pencil-name="Frame 12"]');
  var menu = document.querySelector('[data-pencil-name="Frame 11"]');
  if (!bar || !menu) return;

  menu.id = "mobile-menu";

  var btn = document.createElement("button");
  btn.type = "button";
  btn.className = "mobile-nav-toggle";
  btn.setAttribute("aria-label", "Buka menu");
  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-controls", "mobile-menu");
  btn.innerHTML = "<span></span><span></span><span></span>";
  bar.appendChild(btn);
  bar.classList.add("has-mobile-nav");

  function setOpen(open) {
    bar.classList.toggle("nav-open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.setAttribute("aria-label", open ? "Tutup menu" : "Buka menu");
  }

  btn.addEventListener("click", function () {
    setOpen(!bar.classList.contains("nav-open"));
  });

  menu.addEventListener("click", function (event) {
    if (event.target.closest("a")) setOpen(false);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setOpen(false);
  });
})();

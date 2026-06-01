/* aviosuperficie theme — main.js */
(function () {
  'use strict';

  /* ── Navbar: scroll class ───────────────────────────────── */
  const navbar = document.getElementById('navbar');
  if (navbar) {
    const onScroll = () => {
      navbar.classList.toggle('is-scrolled', window.scrollY > 20);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── Mobile hamburger menu ──────────────────────────────── */
  const burger  = document.getElementById('navburger');
  const navmenu = document.getElementById('navmenu');

  if (burger && navmenu) {
    burger.addEventListener('click', () => {
      const isOpen = burger.classList.toggle('is-open');
      navmenu.classList.toggle('is-open', isOpen);
      burger.setAttribute('aria-expanded', String(isOpen));
    });

    /* Close menu on link click (mobile) */
    navmenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        burger.classList.remove('is-open');
        navmenu.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });

    /* Close on Escape */
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && burger.classList.contains('is-open')) {
        burger.classList.remove('is-open');
        navmenu.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
        burger.focus();
      }
    });
  }

})();

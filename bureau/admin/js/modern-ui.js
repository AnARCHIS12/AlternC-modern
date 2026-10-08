/**
 * AlternC Modern UI - Interactions & Design System 2026
 * Pure JavaScript with full compatibility for existing panels
 */

(function () {
  'use strict';

  // Apply saved theme immediately
  function initTheme() {
    var savedTheme = localStorage.getItem('alternc-theme');
    if (!savedTheme) {
      savedTheme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
  }

  function updateThemeIcon(theme) {
    var icon = document.getElementById('theme-icon');
    if (!icon) return;
    if (theme === 'dark') {
      icon.className = 'fas fa-sun';
      icon.setAttribute('title', 'Passer en mode clair');
    } else {
      icon.className = 'fas fa-moon';
      icon.setAttribute('title', 'Passer en mode sombre');
    }
  }

  function toggleTheme() {
    var currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    var nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', nextTheme);
    localStorage.setItem('alternc-theme', nextTheme);
    updateThemeIcon(nextTheme);
  }

  // Sidebar toggle for desktop & mobile
  function initSidebar() {
    var toggleBtn = document.getElementById('sidebar-toggle');
    var globalContainer = document.getElementById('global');
    var menu = document.getElementById('menu');

    if (!toggleBtn || !globalContainer) return;

    toggleBtn.addEventListener('click', function (e) {
      e.preventDefault();
      if (window.innerWidth <= 992) {
        globalContainer.classList.toggle('sidebar-mobile-open');
      } else {
        globalContainer.classList.toggle('sidebar-collapsed');
        var isCollapsed = globalContainer.classList.contains('sidebar-collapsed');
        localStorage.setItem('alternc-sidebar-collapsed', isCollapsed ? '1' : '0');
      }
    });

    // Restore desktop collapsed state
    if (window.innerWidth > 992 && localStorage.getItem('alternc-sidebar-collapsed') === '1') {
      globalContainer.classList.add('sidebar-collapsed');
    }

    // Close mobile sidebar on backdrop click
    document.addEventListener('click', function (e) {
      if (window.innerWidth <= 992 && globalContainer.classList.contains('sidebar-mobile-open')) {
        if (!menu.contains(e.target) && !toggleBtn.contains(e.target)) {
          globalContainer.classList.remove('sidebar-mobile-open');
        }
      }
    });
  }

  // Spotlight / Quick Search Modal
  var searchIndex = [];
  var selectedIndex = -1;

  function buildSearchIndex() {
    searchIndex = [];
    var menuLinks = document.querySelectorAll('#menu a');
    var seenUrls = {};

    menuLinks.forEach(function (link) {
      var href = link.getAttribute('href');
      if (!href || href.startsWith('javascript:') || href === '#') return;
      var text = (link.textContent || '').trim().replace(/\s+/g, ' ');
      if (!text || seenUrls[href]) return;
      seenUrls[href] = true;

      // Extract icon if present
      var iconClass = 'fa-link';
      var parentBox = link.closest('.menu-box');
      if (parentBox) {
        var boxIcon = parentBox.querySelector('.menu-icon i');
        if (boxIcon) {
          iconClass = boxIcon.className;
        }
      }

      searchIndex.push({
        title: text,
        url: href,
        icon: iconClass
      });
    });

    // Add standard fast actions
    var defaultActions = [
      { title: 'Ajouter un domaine', url: 'dom_add.php', icon: 'fas fa-plus-circle' },
      { title: 'Créer un compte email', url: 'mail_add.php', icon: 'fas fa-envelope' },
      { title: 'Créer une base de données', url: 'sql_add.php', icon: 'fas fa-database' },
      { title: 'Gestionnaire de fichiers', url: 'bro_main.php', icon: 'fas fa-folder-open' },
      { title: 'Mes Quotas', url: 'quota_show.php', icon: 'fas fa-chart-pie' },
      { title: 'Paramètres du compte', url: 'mem_param.php', icon: 'fas fa-user-cog' },
      { title: 'Déconnexion', url: 'mem_logout.php', icon: 'fas fa-sign-out-alt' }
    ];

    defaultActions.forEach(function (item) {
      if (!seenUrls[item.url]) {
        searchIndex.push(item);
        seenUrls[item.url] = true;
      }
    });
  }

  function initQuickSearch() {
    var modal = document.getElementById('quicksearch-modal');
    var input = document.getElementById('quicksearch-input');
    var resultsBox = document.getElementById('quicksearch-results');
    var closeBtn = document.getElementById('quicksearch-close');
    var topbarSearch = document.getElementById('menu-quicksearch');

    if (!modal || !input || !resultsBox) return;

    function openModal() {
      buildSearchIndex();
      modal.style.display = 'flex';
      input.value = '';
      selectedIndex = -1;
      renderResults('');
      setTimeout(function () { input.focus(); }, 50);
    }

    function closeModal() {
      modal.style.display = 'none';
    }

    if (topbarSearch) {
      topbarSearch.addEventListener('focus', function (e) {
        e.preventDefault();
        topbarSearch.blur();
        openModal();
      });
      topbarSearch.addEventListener('click', function (e) {
        e.preventDefault();
        openModal();
      });
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', closeModal);
    }

    modal.addEventListener('click', function (e) {
      if (e.target === modal) closeModal();
    });

    // Keyboard shortcut: Ctrl+K or Cmd+K
    window.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (modal.style.display === 'flex') {
          closeModal();
        } else {
          openModal();
        }
      } else if (e.key === 'Escape' && modal.style.display === 'flex') {
        closeModal();
      }
    });

    function renderResults(query) {
      resultsBox.innerHTML = '';
      var q = query.toLowerCase().trim();
      var filtered = searchIndex.filter(function (item) {
        return !q || item.title.toLowerCase().indexOf(q) !== -1 || item.url.toLowerCase().indexOf(q) !== -1;
      }).slice(0, 8);

      if (filtered.length === 0) {
        resultsBox.innerHTML = '<div class="quicksearch-empty"><i class="fas fa-search"></i> Aucun résultat trouvé</div>';
        selectedIndex = -1;
        return;
      }

      filtered.forEach(function (item, idx) {
        var a = document.createElement('a');
        a.href = item.url;
        a.className = 'quicksearch-item' + (idx === 0 ? ' is-selected' : '');
        a.innerHTML = '<span class="item-icon"><i class="' + item.icon + '"></i></span>' +
                      '<span class="item-title">' + item.title + '</span>' +
                      '<span class="item-url">' + item.url + '</span>';
        a.addEventListener('mouseenter', function () {
          var items = resultsBox.querySelectorAll('.quicksearch-item');
          items.forEach(function (el) { el.classList.remove('is-selected'); });
          a.classList.add('is-selected');
          selectedIndex = idx;
        });
        resultsBox.appendChild(a);
      });
      selectedIndex = 0;
    }

    input.addEventListener('input', function () {
      renderResults(input.value);
    });

    input.addEventListener('keydown', function (e) {
      var items = resultsBox.querySelectorAll('.quicksearch-item');
      if (items.length === 0) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedIndex = (selectedIndex + 1) % items.length;
        items.forEach(function (el, i) {
          el.classList.toggle('is-selected', i === selectedIndex);
        });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedIndex = (selectedIndex - 1 + items.length) % items.length;
        items.forEach(function (el, i) {
          el.classList.toggle('is-selected', i === selectedIndex);
        });
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedIndex >= 0 && items[selectedIndex]) {
          window.location.href = items[selectedIndex].getAttribute('href');
        }
      }
    });
  }

  // DOM ready initialization
  document.addEventListener('DOMContentLoaded', function () {
    initTheme();

    var themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', toggleTheme);
    }

    initSidebar();
    initQuickSearch();
  });

})();

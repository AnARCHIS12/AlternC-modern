#!/usr/bin/env python3
"""
Generate AlternC modern offline-first multilingual documentation portal.
Supports Esperanto (default), Français, English, and Español.
Zero external CDN, zero emojis, zero 'souverain' terminology.
"""

import json

html_template = """<!DOCTYPE html>
<html lang="eo" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title data-i18n="docTitle">AlternC Dokumentaro | Libera & Memmastrumata Platformo</title>
  <style>
    :root {
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

      /* Light Theme */
      --bg-page: #f8fafc;
      --bg-surface: #ffffff;
      --bg-sidebar: #f1f5f9;
      --bg-card: #ffffff;
      --bg-code: #0f172a;
      --border-color: #e2e8f0;

      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --text-link: #059669;

      --accent: #059669;
      --accent-hover: #047857;
      --accent-light: #ecfdf5;

      --success: #10b981;
      --success-bg: #ecfdf5;
      --warning: #f59e0b;
      --warning-bg: #fffbeb;
      --danger: #ef4444;
      --danger-bg: #fef2f2;

      --sidebar-width: 280px;
      --toc-width: 240px;
      --header-height: 64px;
      --radius: 10px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.08);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
    }

    [data-theme="dark"] {
      --bg-page: #090a0f;
      --bg-surface: #11131a;
      --bg-sidebar: #0c0e14;
      --bg-card: #151822;
      --bg-code: #050608;
      --border-color: #212634;

      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --text-link: #34d399;

      --accent: #10b981;
      --accent-hover: #34d399;
      --accent-light: rgba(16, 185, 129, 0.12);

      --success-bg: rgba(16, 185, 129, 0.12);
      --warning-bg: rgba(245, 158, 11, 0.12);
      --danger-bg: rgba(239, 68, 68, 0.12);

      --shadow-sm: 0 1px 3px rgba(0,0,0,0.5);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.4);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.5);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-page);
      color: var(--text-primary);
      line-height: 1.65;
      -webkit-font-smoothing: antialiased;
    }

    a { color: var(--text-link); text-decoration: none; transition: color 0.15s ease; }
    a:hover { text-decoration: underline; }

    /* Top Navigation */
    .header {
      position: sticky;
      top: 0;
      height: var(--header-height);
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 2rem;
      z-index: 100;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-weight: 700;
      font-size: 1.15rem;
      color: var(--text-primary);
    }

    .brand-logo {
      height: 28px;
      border-radius: 4px;
      display: block;
    }

    .brand-badge {
      font-size: 0.7rem;
      background: var(--accent-light);
      color: var(--accent);
      padding: 0.2rem 0.5rem;
      border-radius: 9999px;
      font-weight: 600;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    /* Language Switcher */
    .lang-switcher {
      display: flex;
      align-items: center;
      background: var(--bg-page);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 2px;
      gap: 2px;
    }

    .lang-btn {
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.25rem 0.55rem;
      border-radius: calc(var(--radius) - 2px);
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .lang-btn:hover {
      color: var(--text-primary);
    }

    .lang-btn.active {
      background: var(--accent);
      color: #ffffff;
    }

    .search-bar {
      position: relative;
      display: flex;
      align-items: center;
    }

    .search-bar svg {
      position: absolute;
      left: 12px;
      color: var(--text-muted);
      width: 14px;
      height: 14px;
    }

    .search-input {
      padding: 0.45rem 1rem 0.45rem 2.25rem;
      border-radius: 9999px;
      border: 1px solid var(--border-color);
      background: var(--bg-page);
      color: var(--text-primary);
      font-size: 0.875rem;
      width: 220px;
      outline: none;
      transition: all 0.15s ease;
    }

    .search-input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-light);
      width: 280px;
    }

    .btn-icon {
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      width: 36px;
      height: 36px;
      border-radius: var(--radius);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .btn-icon svg {
      width: 16px;
      height: 16px;
    }

    .btn-icon:hover {
      background: var(--bg-page);
      color: var(--accent);
      border-color: var(--accent);
    }

    /* Layout */
    .docs-container {
      display: flex;
      min-height: calc(100vh - var(--header-height));
      max-width: 1600px;
      margin: 0 auto;
    }

    /* Sidebar Navigation */
    .sidebar {
      width: var(--sidebar-width);
      min-width: var(--sidebar-width);
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border-color);
      padding: 1.5rem 1.25rem;
      height: calc(100vh - var(--header-height));
      position: sticky;
      top: var(--header-height);
      overflow-y: auto;
    }

    .sidebar-group {
      margin-bottom: 1.5rem;
    }

    .sidebar-title {
      font-size: 0.75rem;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 0.75rem;
      padding-left: 0.5rem;
    }

    .sidebar-menu {
      list-style: none;
    }

    .sidebar-link {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      padding: 0.45rem 0.65rem;
      font-size: 0.875rem;
      color: var(--text-secondary);
      border-radius: var(--radius);
      transition: all 0.15s ease;
      font-weight: 500;
    }

    .sidebar-link svg {
      width: 15px;
      height: 15px;
    }

    .sidebar-link:hover {
      background: var(--accent-light);
      color: var(--accent);
      text-decoration: none;
    }

    .sidebar-link.active {
      background: var(--accent);
      color: #ffffff;
    }

    .sidebar-link.active svg {
      color: #ffffff;
    }

    /* Main Content */
    .main-content {
      flex: 1;
      padding: 2.5rem 3.5rem;
      max-width: 950px;
    }

    /* Table of Contents */
    .toc {
      width: var(--toc-width);
      min-width: var(--toc-width);
      padding: 2.5rem 1.5rem;
      position: sticky;
      top: var(--header-height);
      height: calc(100vh - var(--header-height));
      overflow-y: auto;
    }

    .toc-title {
      font-size: 0.8rem;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 0.75rem;
    }

    .toc-list {
      list-style: none;
      font-size: 0.825rem;
      border-left: 1px solid var(--border-color);
    }

    .toc-item {
      padding-left: 0.85rem;
      margin: 0.4rem 0;
    }

    .toc-link {
      color: var(--text-secondary);
      display: block;
      transition: color 0.15s ease;
    }

    .toc-link:hover, .toc-link.active {
      color: var(--accent);
      text-decoration: none;
    }

    /* Typography & Sections */
    h1 {
      font-size: 2.25rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin-bottom: 0.75rem;
      line-height: 1.2;
    }

    .lead {
      font-size: 1.15rem;
      color: var(--text-secondary);
      margin-bottom: 2rem;
      line-height: 1.6;
    }

    h2 {
      font-size: 1.5rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin: 2.5rem 0 1rem 0;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    p {
      margin-bottom: 1.25rem;
      color: var(--text-secondary);
    }

    /* Code Blocks */
    .code-box {
      background: var(--bg-code);
      color: #f8fafc;
      border-radius: var(--radius);
      border: 1px solid var(--border-color);
      margin: 1.25rem 0;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
    }

    .code-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.5rem 1rem;
      background: rgba(255, 255, 255, 0.05);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 0.75rem;
      font-family: var(--font-mono);
      color: #94a3b8;
    }

    .code-copy-btn {
      background: transparent;
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #94a3b8;
      font-size: 0.75rem;
      padding: 0.2rem 0.55rem;
      border-radius: 4px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.15s ease;
    }

    .code-copy-btn:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.3);
    }

    pre {
      padding: 1rem;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      overflow-x: auto;
      line-height: 1.5;
    }

    code {
      font-family: var(--font-mono);
      font-size: 0.85em;
      background: var(--bg-code);
      color: var(--accent);
      padding: 0.15rem 0.35rem;
      border-radius: 4px;
    }

    /* Callout */
    .callout {
      border-radius: var(--radius);
      padding: 1rem 1.25rem;
      margin: 1.5rem 0;
      display: flex;
      gap: 1rem;
      align-items: flex-start;
      border: 1px solid transparent;
    }

    .callout-tip {
      background: var(--success-bg);
      border-color: rgba(16, 185, 129, 0.25);
      color: var(--text-primary);
    }

    .callout-tip svg {
      color: var(--success);
      width: 20px;
      height: 20px;
      flex-shrink: 0;
      margin-top: 2px;
    }

    .callout-info {
      background: var(--accent-light);
      border-color: rgba(16, 185, 129, 0.25);
      color: var(--text-primary);
    }

    .callout-info svg {
      color: var(--accent);
      width: 20px;
      height: 20px;
      flex-shrink: 0;
      margin-top: 2px;
    }

    .callout-title {
      font-weight: 600;
      font-size: 0.9rem;
      margin-bottom: 0.25rem;
    }

    .callout-content p {
      margin: 0;
      font-size: 0.875rem;
      color: var(--text-secondary);
    }

    /* Table */
    .table-container {
      overflow-x: auto;
      margin: 1.5rem 0;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      overflow: hidden;
      font-size: 0.875rem;
      background: var(--bg-surface);
    }

    th {
      background: var(--bg-page);
      color: var(--text-primary);
      text-align: left;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-color);
      font-weight: 600;
    }

    td {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-secondary);
    }

    tr:last-child td { border-bottom: none; }

    /* Feature Grid */
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.25rem;
      margin: 1.5rem 0;
    }

    .card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 1.25rem;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s ease;
    }

    .card:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .card-icon {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: var(--accent-light);
      color: var(--accent);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 0.85rem;
    }

    .card-icon svg { width: 18px; height: 18px; }

    .card-title {
      font-weight: 600;
      font-size: 1rem;
      margin-bottom: 0.35rem;
      color: var(--text-primary);
    }

    .card-desc {
      font-size: 0.85rem;
      color: var(--text-secondary);
      margin: 0;
    }

    @media (max-width: 1100px) {
      .toc { display: none; }
      .main-content { padding: 2rem 1.5rem; }
    }

    @media (max-width: 768px) {
      .sidebar { display: none; }
      .grid-2 { grid-template-columns: 1fr; }
      .search-input { width: 140px; }
      .search-input:focus { width: 180px; }
      .header { padding: 0 1rem; }
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header class="header">
    <div class="brand">
      <img src="logo.png" alt="AlternC" class="brand-logo" />
      <span class="brand-badge" data-i18n="brandBadge">Memmastrumado & Komunaĵoj</span>
    </div>

    <div class="header-actions">
      <!-- Multilingual Switcher -->
      <div class="lang-switcher">
        <button class="lang-btn active" data-lang="eo" title="Esperanto">EO</button>
        <button class="lang-btn" data-lang="fr" title="Français">FR</button>
        <button class="lang-btn" data-lang="en" title="English">EN</button>
        <button class="lang-btn" data-lang="es" title="Español">ES</button>
      </div>

      <div class="search-bar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="doc-search" class="search-input" data-i18n-placeholder="searchPlaceholder" placeholder="Serĉi en la dokumentaro..." />
      </div>

      <button id="theme-btn" class="btn-icon" title="Baskuli etoson">
        <svg id="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
      </button>

      <a href="https://github.com/AlternC/AlternC" target="_blank" class="btn-icon" title="Git">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
      </a>
    </div>
  </header>

  <!-- Container -->
  <div class="docs-container">

    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-group">
        <div class="sidebar-title" data-i18n="sidebarGroup1">Ekfunkciigo & Fundamento</div>
        <ul class="sidebar-menu">
          <li><a href="#introduction" class="sidebar-link active"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg> <span data-i18n="navIntro">Enkonduko</span></a></li>
          <li><a href="#anticapitalisme" class="sidebar-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg> <span data-i18n="navEthics">Etiko & Kontraŭkapitalismo</span></a></li>
          <li><a href="#docker-install" class="sidebar-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg> <span data-i18n="navDocker">Docker Instalado</span></a></li>
          <li><a href="#port-isolation" class="sidebar-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="16" y="16" width="6" height="6" rx="1"></rect><rect x="2" y="16" width="6" height="6" rx="1"></rect><rect x="9" y="2" width="6" height="6" rx="1"></rect><path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"></path><path d="M12 12V8"></path></svg> <span data-i18n="navPorts">Pordo-Izolado</span></a></li>
        </ul>
      </div>

      <div class="sidebar-group">
        <div class="sidebar-title" data-i18n="sidebarGroup2">Arkitekturo & Deplojo</div>
        <ul class="sidebar-menu">
          <li><a href="#frontend-2026" class="sidebar-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="13.5" cy="6.5" r=".5"></circle><circle cx="17.5" cy="10.5" r=".5"></circle><circle cx="8.5" cy="7.5" r=".5"></circle><circle cx="6.5" cy="12.5" r=".5"></circle><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"></path></svg> <span data-i18n="navUI">Fasado & Desegno 2026</span></a></li>
          <li><a href="#reverse-proxy" class="sidebar-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg> <span data-i18n="navProxy">Nginx Reversa Prokurilo</span></a></li>
          <li><a href="#env-variables" class="sidebar-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line></svg> <span data-i18n="navEnv">Medivariabloj .env</span></a></li>
          <li><a href="#faq" class="sidebar-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg> <span data-i18n="navFaq">Oftaj Demandoj</span></a></li>
        </ul>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      
      <!-- Section: Introduction -->
      <section id="introduction">
        <h1 data-i18n="introTitle">AlternC Dokumentaro</h1>
        <p class="lead" data-i18n="introLead">Emancipa, memmastrumata kaj libera platformo por komuna gastigado, funkcianta per PHP 8.3 kaj MariaDB en izolitaj ujoj sen pordo-konfliktoj.</p>

        <div class="grid-2">
          <div class="card">
            <div class="card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg></div>
            <div class="card-title" data-i18n="featEthicsTitle">Memmastrumado & Komunaĵoj</div>
            <p class="card-desc" data-i18n="featEthicsDesc">Liberiĝo disde Big Tech, libera kodo copyleft kaj horizontala regado de servilaj resursoj.</p>
          </div>
          <div class="card">
            <div class="card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg></div>
            <div class="card-title" data-i18n="featDockerTitle">Docker PHP 8.3</div>
            <p class="card-desc" data-i18n="featDockerDesc">Moderna ujo kun PHP 8.3, MariaDB 10.11 LTS kaj strikta daŭreco de volumoj.</p>
          </div>
          <div class="card">
            <div class="card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="16" y="16" width="6" height="6" rx="1"></rect><rect x="2" y="16" width="6" height="6" rx="1"></rect><rect x="9" y="2" width="6" height="6" rx="1"></rect><path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"></path><path d="M12 12V8"></path></svg></div>
            <div class="card-title" data-i18n="featPortsTitle">Nula Pordo-Konflikto</div>
            <p class="card-desc" data-i18n="featPortsDesc">Pordoj HTTP (8080), SSL (8443) kaj DB (3307) plene izolitaj de ekzistantaj servoj.</p>
          </div>
          <div class="card">
            <div class="card-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></div>
            <div class="card-title" data-i18n="featSpotlightTitle">Navigado & Spotlight</div>
            <p class="card-desc" data-i18n="featSpotlightDesc">Komand-paletro (Stirklavo+K), sobra etoso kaj dinamika sinkronigo.</p>
          </div>
        </div>
      </section>

      <!-- Section: Anticapitalisme -->
      <section id="anticapitalisme">
        <h2 data-i18n="ethicsTitle">Etiko Kontraŭkapitalisma & Ciferecaj Komunaĵoj</h2>
        <p data-i18n="ethicsLead">AlternC naskiĝis kaj vivas kiel kolektiva rezisto kontraŭ la komercaj bariloj kaj monopoloj de la gvata kapitalismo.</p>

        <div class="grid-2">
          <div class="card">
            <div class="card-title" data-i18n="ethicsCard1Title">Rifuzo de Big Tech & Komercaj Nuboj</div>
            <p class="card-desc" data-i18n="ethicsCard1Desc">Batalo kontraŭ privataj monopoloj (AWS, Google Cloud, Azure) kiuj baras la reton kaj komercigas personajn datumojn. AlternC ebligas plenan aŭtonomion.</p>
          </div>
          <div class="card">
            <div class="card-title" data-i18n="ethicsCard2Title">Kolektiva Memmastrumado</div>
            <p class="card-desc" data-i18n="ethicsCard2Desc">Horizontala administrado de serviloj, retpoŝtoj kaj domajnoj sen dependeco de komercaj kompanioj.</p>
          </div>
          <div class="card">
            <div class="card-title" data-i18n="ethicsCard3Title">Ciferecaj Komunaĵoj</div>
            <p class="card-desc" data-i18n="ethicsCard3Desc">100% libera fontkodo (GPLv2+), malfermitaj protokoloj, nula ekstera CDN kaj nula telemetrio.</p>
          </div>
          <div class="card">
            <div class="card-title" data-i18n="ethicsCard4Title">Frugaleco & Ekologia Sobrieco</div>
            <p class="card-desc" data-i18n="ethicsCard4Desc">Malpeza arkitekturo funkcianta tute loke (offline-first), respektante komputilojn kaj rimedojn.</p>
          </div>
        </div>
      </section>

      <!-- Section: Docker Installation -->
      <section id="docker-install">
        <h2 data-i18n="dockerTitle">Instalado per Docker en 1 Komando</h2>
        <p data-i18n="dockerDesc">Moderna komandlinia skripto aŭtomate konfiguras la medion, skanas liberajn pordojn kaj lanĉas la ujojn.</p>

        <div class="code-box">
          <div class="code-header">
            <span data-i18n="dockerHeader">bash — Aŭtomata deplojo</span>
            <button class="code-copy-btn" onclick="copyCode(this)" data-i18n="btnCopy">Kopii</button>
          </div>
          <pre><code>chmod +x install.sh
./install.sh</code></pre>
        </div>

        <div class="callout callout-tip">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          <div class="callout-content">
            <div class="callout-title" data-i18n="dockerCalloutTitle">Seninteraga deplojo (CI/CD)</div>
            <p data-i18n-html="dockerCalloutDesc">Por rekta instalado sen demandoj: <code>./install.sh -y</code>.</p>
          </div>
        </div>
      </section>

      <!-- Section: Port Isolation -->
      <section id="port-isolation">
        <h2 data-i18n="portsTitle">Pordo-Izolado</h2>
        <p data-i18n="portsDesc">La Docker-arkitekturo izolas ĉiun pordon per la dosiero .env por kunekzisti kun aliaj servoj:</p>

        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th data-i18n="thService">Servo</th>
                <th data-i18n="thHostPort">Defaŭlta Gastiga Pordo</th>
                <th data-i18n="thContainerPort">Uja Pordo</th>
                <th data-i18n="thEnvVar">Medivariablo</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong data-i18n="serviceWebHttp">TTT HTTP</strong></td>
                <td><code>8080</code></td>
                <td><code>80</code></td>
                <td><code>ALTERNC_HTTP_PORT</code></td>
              </tr>
              <tr>
                <td><strong data-i18n="serviceWebHttps">TTT HTTPS (SSL)</strong></td>
                <td><code>8443</code></td>
                <td><code>443</code></td>
                <td><code>ALTERNC_HTTPS_PORT</code></td>
              </tr>
              <tr>
                <td><strong data-i18n="serviceDb">MariaDB / MySQL</strong></td>
                <td><code>3307</code></td>
                <td><code>3306</code></td>
                <td><code>ALTERNC_MYSQL_PORT</code></td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Section: Frontend 2026 -->
      <section id="frontend-2026">
        <h2 data-i18n="uiTitle">Fasado & Desegno 2026</h2>
        <p data-i18n="uiDesc">La administrejo disponas pri moderna, adaptiĝema kaj sobra fasado:</p>
        
        <ul style="padding-left: 1.5rem; margin-bottom: 1.5rem; color: var(--text-secondary);">
          <li data-i18n-html="uiPoint1"><strong>Strukturo</strong>: Flanka navigado kun lokaj SVG-vektoroj, supra stirbreto kun servilaj indikiloj.</li>
          <li data-i18n-html="uiPoint2"><strong>Malhela / Hela Etoso</strong>: Tuja ŝanĝo memorita en <code>localStorage</code> sen flagrado.</li>
          <li data-i18n-html="uiPoint3"><strong>Tabelaj Datumoj</strong>: Aeraj tabeloj, alireblaj koloroj kaj glataj kontrastoj.</li>
        </ul>

        <div class="callout callout-info">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
          <div class="callout-content">
            <div class="callout-title" data-i18n="uiSpotlightTitle">Komand-paletro (Stirklavo+K)</div>
            <p data-i18n="uiSpotlightDesc">Premu Ctrl+K aŭ Cmd+K sur iu ajn paĝo por malfermi la rapidan serĉilon Spotlight.</p>
          </div>
        </div>
      </section>

      <!-- Section: Reverse Proxy -->
      <section id="reverse-proxy">
        <h2 data-i18n="proxyTitle">Nginx Reversa Prokurilo</h2>
        <p data-i18n="proxyDesc">Por publikigi AlternC sur publika subdomajno per Nginx:</p>

        <div class="code-box">
          <div class="code-header">
            <span data-i18n="proxyHeader">nginx.conf — VirtualHost Reversa Prokurilo</span>
            <button class="code-copy-btn" onclick="copyCode(this)" data-i18n="btnCopy">Kopii</button>
          </div>
          <pre><code>server {
    listen 80;
    server_name panel.example.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}</code></pre>
        </div>
      </section>

      <!-- Section: Environment Variables -->
      <section id="env-variables">
        <h2 data-i18n="envTitle">Medivariabloj .env</h2>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th data-i18n="thVar">Variablo</th>
                <th data-i18n="thDefault">Defaŭlto</th>
                <th data-i18n="thDesc">Priskribo</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>ALTERNC_HTTP_PORT</code></td>
                <td><code>8080</code></td>
                <td data-i18n="envHttpPort">Gastiga HTTP-pordo.</td>
              </tr>
              <tr>
                <td><code>ALTERNC_HTTPS_PORT</code></td>
                <td><code>8443</code></td>
                <td data-i18n="envHttpsPort">Gastiga HTTPS-pordo (SSL).</td>
              </tr>
              <tr>
                <td><code>ALTERNC_MYSQL_PORT</code></td>
                <td><code>3307</code></td>
                <td data-i18n="envMysqlPort">Ekstera MariaDB-pordo.</td>
              </tr>
              <tr>
                <td><code>ALTERNC_ADMIN_USER</code></td>
                <td><code>admin</code></td>
                <td data-i18n="envAdminUser">Administra uzantnomo.</td>
              </tr>
              <tr>
                <td><code>ALTERNC_ADMIN_PASS</code></td>
                <td><em data-i18n="envAdminPassVal">generita</em></td>
                <td data-i18n="envAdminPass">Administra pasvorto.</td>
              </tr>
              <tr>
                <td><code>DB_NAME</code></td>
                <td><code>alternc</code></td>
                <td data-i18n="envDbName">Datumbaza nomo.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Section: FAQ -->
      <section id="faq">
        <h2 data-i18n="faqTitle">Oftaj Demandoj & Helpo</h2>
        <div class="card" style="margin-bottom: 1rem;">
          <div class="card-title" data-i18n="faqQ1">Kiel vidi la protokolojn rekte?</div>
          <p class="card-desc" data-i18n-html="faqA1">Rulu: <code>docker compose logs -f</code>.</p>
        </div>
        <div class="card" style="margin-bottom: 1rem;">
          <div class="card-title" data-i18n="faqQ2">Kiel ŝanĝi pordon sen reinstalo?</div>
          <p class="card-desc" data-i18n-html="faqA2">Ŝanĝu <code>ALTERNC_HTTP_PORT</code> en via <code>.env</code>, poste rulu: <code>docker compose up -d</code>.</p>
        </div>
      </section>

    </main>

    <!-- Right Table of Contents -->
    <aside class="toc">
      <div class="toc-title" data-i18n="tocTitle">Sur ĉi tiu paĝo</div>
      <ul class="toc-list">
        <li class="toc-item"><a href="#introduction" class="toc-link" data-i18n="navIntro">Enkonduko</a></li>
        <li class="toc-item"><a href="#anticapitalisme" class="toc-link" data-i18n="navEthics">Etiko & Kontraŭkapitalismo</a></li>
        <li class="toc-item"><a href="#docker-install" class="toc-link" data-i18n="navDocker">Docker Instalado</a></li>
        <li class="toc-item"><a href="#port-isolation" class="toc-link" data-i18n="navPorts">Pordo-Izolado</a></li>
        <li class="toc-item"><a href="#frontend-2026" class="toc-link" data-i18n="navUI">Fasado & Desegno 2026</a></li>
        <li class="toc-item"><a href="#reverse-proxy" class="toc-link" data-i18n="navProxy">Reversa Prokurilo</a></li>
        <li class="toc-item"><a href="#env-variables" class="toc-link" data-i18n="navEnv">Medivariabloj</a></li>
        <li class="toc-item"><a href="#faq" class="toc-link" data-i18n="navFaq">Oftaj Demandoj</a></li>
      </ul>
    </aside>

  </div>

  <script>
    /* Multilingual i18n Dictionary */
    const translations = {
      eo: {
        docTitle: "AlternC Dokumentaro | Libera & Memmastrumata Platformo",
        brandBadge: "Memmastrumado & Komunaĵoj",
        searchPlaceholder: "Serĉi en la dokumentaro...",
        sidebarGroup1: "Ekfunkciigo & Fundamento",
        sidebarGroup2: "Arkitekturo & Deplojo",
        navIntro: "Enkonduko",
        navEthics: "Etiko & Kontraŭkapitalismo",
        navDocker: "Docker Instalado",
        navPorts: "Pordo-Izolado",
        navUI: "Fasado & Desegno 2026",
        navProxy: "Nginx Reversa Prokurilo",
        navEnv: "Medivariabloj .env",
        navFaq: "Oftaj Demandoj",
        introTitle: "AlternC Dokumentaro",
        introLead: "Emancipa, memmastrumata kaj libera platformo por komuna gastigado, funkcianta per PHP 8.3 kaj MariaDB en izolitaj ujoj sen pordo-konfliktoj.",
        featEthicsTitle: "Memmastrumado & Komunaĵoj",
        featEthicsDesc: "Liberiĝo disde Big Tech, libera kodo copyleft kaj horizontala regado de servilaj resursoj.",
        featDockerTitle: "Docker PHP 8.3",
        featDockerDesc: "Moderna ujo kun PHP 8.3, MariaDB 10.11 LTS kaj strikta daŭreco de volumoj.",
        featPortsTitle: "Nula Pordo-Konflikto",
        featPortsDesc: "Pordoj HTTP (8080), SSL (8443) kaj DB (3307) plene izolitaj de ekzistantaj servoj.",
        featSpotlightTitle: "Navigado & Spotlight",
        featSpotlightDesc: "Komand-paletro (Stirklavo+K), sobra etoso kaj dinamika sinkronigo.",
        ethicsTitle: "Etiko Kontraŭkapitalisma & Ciferecaj Komunaĵoj",
        ethicsLead: "AlternC naskiĝis kaj vivas kiel kolektiva rezisto kontraŭ la komercaj bariloj kaj monopoloj de la gvata kapitalismo.",
        ethicsCard1Title: "Rifuzo de Big Tech & Komercaj Nuboj",
        ethicsCard1Desc: "Batalo kontraŭ privataj monopoloj (AWS, Google Cloud, Azure) kiuj baras la reton kaj komercigas personajn datumojn. AlternC ebligas plenan aŭtonomion.",
        ethicsCard2Title: "Kolektiva Memmastrumado",
        ethicsCard2Desc: "Horizontala administrado de serviloj, retpoŝtoj kaj domajnoj sen dependeco de komercaj kompanioj.",
        ethicsCard3Title: "Ciferecaj Komunaĵoj",
        ethicsCard3Desc: "100% libera fontkodo (GPLv2+), malfermitaj protokoloj, nula ekstera CDN kaj nula telemetrio.",
        ethicsCard4Title: "Frugaleco & Ekologia Sobrieco",
        ethicsCard4Desc: "Malpeza arkitekturo funkcianta tute loke (offline-first), respektante komputilojn kaj rimedojn.",
        dockerTitle: "Instalado per Docker en 1 Komando",
        dockerDesc: "Moderna komandlinia skripto aŭtomate konfiguras la medion, skanas liberajn pordojn kaj lanĉas la ujojn.",
        dockerHeader: "bash — Aŭtomata deplojo",
        btnCopy: "Kopii",
        btnCopied: "Kopiita!",
        dockerCalloutTitle: "Seninteraga deplojo (CI/CD)",
        dockerCalloutDesc: "Por rekta instalado sen demandoj: <code>./install.sh -y</code>.",
        portsTitle: "Pordo-Izolado",
        portsDesc: "La Docker-arkitekturo izolas ĉiun pordon per la dosiero .env por kunekzisti kun aliaj servoj:",
        thService: "Servo",
        thHostPort: "Defaŭlta Gastiga Pordo",
        thContainerPort: "Uja Pordo",
        thEnvVar: "Medivariablo",
        serviceWebHttp: "TTT HTTP",
        serviceWebHttps: "TTT HTTPS (SSL)",
        serviceDb: "MariaDB / MySQL",
        uiTitle: "Fasado & Desegno 2026",
        uiDesc: "La administrejo disponas pri moderna, adaptiĝema kaj sobra fasado:",
        uiPoint1: "<strong>Strukturo</strong>: Flanka navigado kun lokaj SVG-vektoroj, supra stirbreto kun servilaj indikiloj.",
        uiPoint2: "<strong>Malhela / Hela Etoso</strong>: Tuja ŝanĝo memorita en <code>localStorage</code> sen flagrado.",
        uiPoint3: "<strong>Tabelaj Datumoj</strong>: Aeraj tabeloj, alireblaj koloroj kaj glataj kontrastoj.",
        uiSpotlightTitle: "Komand-paletro (Stirklavo+K)",
        uiSpotlightDesc: "Premu Ctrl+K aŭ Cmd+K sur iu ajn paĝo por malfermi la rapidan serĉilon Spotlight.",
        proxyTitle: "Nginx Reversa Prokurilo",
        proxyDesc: "Por publikigi AlternC sur publika subdomajno per Nginx:",
        proxyHeader: "nginx.conf — VirtualHost Reversa Prokurilo",
        envTitle: "Medivariabloj .env",
        thVar: "Variablo",
        thDefault: "Defaŭlto",
        thDesc: "Priskribo",
        envHttpPort: "Gastiga HTTP-pordo.",
        envHttpsPort: "Gastiga HTTPS-pordo (SSL).",
        envMysqlPort: "Ekstera MariaDB-pordo.",
        envAdminUser: "Administra uzantnomo.",
        envAdminPassVal: "generita",
        envAdminPass: "Administra pasvorto.",
        envDbName: "Datumbaza nomo.",
        faqTitle: "Oftaj Demandoj & Helpo",
        faqQ1: "Kiel vidi la protokolojn rekte?",
        faqA1: "Rulu: <code>docker compose logs -f</code>.",
        faqQ2: "Kiel ŝanĝi pordon sen reinstalo?",
        faqA2: "Ŝanĝu <code>ALTERNC_HTTP_PORT</code> en via <code>.env</code>, poste rulu: <code>docker compose up -d</code>.",
        tocTitle: "Sur ĉi tiu paĝo"
      },
      fr: {
        docTitle: "Documentation AlternC | Plateforme Libre & Autogérée",
        brandBadge: "Autogestion & Communs",
        searchPlaceholder: "Rechercher dans la doc...",
        sidebarGroup1: "Démarrage & Fondations",
        sidebarGroup2: "Architecture & Déploiement",
        navIntro: "Introduction",
        navEthics: "Éthique & Anticapitalisme",
        navDocker: "Installation Docker",
        navPorts: "Isolation des ports",
        navUI: "UI & Design System 2026",
        navProxy: "Nginx & Reverse Proxy",
        navEnv: "Variables d'environnement",
        navFaq: "FAQ & Dépannage",
        introTitle: "Documentation AlternC",
        introLead: "Plateforme d'hébergement mutualisé autogérée et émancipatrice, propulsée par PHP 8.3 et MariaDB en conteneurs étanches sans aucun conflit de port.",
        featEthicsTitle: "Autogestion & Communs",
        featEthicsDesc: "Émancipation face aux géants de la Big Tech, logiciels libres copyleft et gestion horizontale des infrastructures.",
        featDockerTitle: "Docker PHP 8.3",
        featDockerDesc: "Conteneurisation moderne sous PHP 8.3, MariaDB 10.11 LTS et persistance stricte des volumes de données.",
        featPortsTitle: "Zéro Conflit de Port",
        featPortsDesc: "Ports HTTP (8080), SSL (8443) et DB (3307) isolés. Ne monopolise ni ne bloque aucun service hôte existant.",
        featSpotlightTitle: "Navigation & Spotlight",
        featSpotlightDesc: "Palette de commande (Ctrl+K), thème sombre/clair sobre et synchronisation interactive fluide.",
        ethicsTitle: "Éthique Anticapitaliste & Communs Numériques",
        ethicsLead: "AlternC s'ancre dans une volonté d'émancipation collective, d'autogestion et de refus catégorique des logiques marchandes prédatrices du capitalisme de surveillance.",
        ethicsCard1Title: "Refus de la Big Tech & Enclosures Marchandes",
        ethicsCard1Desc: "Rejet des monopoles propriétaires (AWS, Google Cloud, Microsoft Azure) qui privatisent le web et marchandisent les données. AlternC permet une autonomie totale.",
        ethicsCard2Title: "Autogestion & Réappropriation Populaire",
        ethicsCard2Desc: "Horizontalité, gestion collective des ressources et maîtrise technique directe des serveurs sans intermédiaires commerciaux ni tutelle corporatiste.",
        ethicsCard3Title: "Défense Inconditionnelle des Communs",
        ethicsCard3Desc: "Code source 100% libre sous licence copyleft (GPLv2+), formats ouverts, protocoles interopérables, zéro CDN externe et zéro télémétrie.",
        ethicsCard4Title: "Frugalité & Sobriété Émancipatrice",
        ethicsCard4Desc: "Architecture légère, zéro pistage publicitaire, fonctionnement hors-ligne (offline-first) respectueux des machines et de l'environnement.",
        dockerTitle: "Installation Docker en 1 Commande",
        dockerDesc: "Un script d'installation moderne en ligne de commande configure l'environnement, inspecte les ports libres sur la machine hôte et déploie les conteneurs.",
        dockerHeader: "bash — Déploiement guidé",
        btnCopy: "Copier",
        btnCopied: "Copié !",
        dockerCalloutTitle: "Déploiement non-interactif (Automated / CI/CD)",
        dockerCalloutDesc: "Pour un déploiement direct sans interaction : <code>./install.sh -y</code>.",
        portsTitle: "Isolation des Ports",
        portsDesc: "L'architecture Docker sépare chaque port via le fichier .env afin de cohabiter avec tout autre serveur :",
        thService: "Service",
        thHostPort: "Port Hôte par défaut",
        thContainerPort: "Port Conteneur",
        thEnvVar: "Variable d'environnement",
        serviceWebHttp: "Web HTTP",
        serviceWebHttps: "Web HTTPS (SSL)",
        serviceDb: "MariaDB / MySQL",
        uiTitle: "Interface & Design System 2026",
        uiDesc: "Le panneau d'administration dispose d'un design contemporain, fluide et ergonomique :",
        uiPoint1: "<strong>Architecture Layout</strong> : Sidebar sticky avec icônes SVG locales, Topbar avec badges serveurs et profil.",
        uiPoint2: "<strong>Dark / Light Mode</strong> : Bascule de thème instantanée stockée dans <code>localStorage</code> sans scintillement.",
        uiPoint3: "<strong>Données tabulaires</strong> : Tableaux aérés, zébrures douces, hover states et contrastes accessibles.",
        uiSpotlightTitle: "Palette de commande (Ctrl+K)",
        uiSpotlightDesc: "Appuyez sur Ctrl+K ou Cmd+K sur n'importe quelle page pour ouvrir la recherche rapide Spotlight.",
        proxyTitle: "Intégration Reverse Proxy (Nginx)",
        proxyDesc: "Pour exposer AlternC sur un sous-domaine public via un reverse proxy Nginx :",
        proxyHeader: "nginx.conf — VirtualHost Reverse Proxy",
        envTitle: "Référence des Variables .env",
        thVar: "Variable",
        thDefault: "Défaut",
        thDesc: "Description",
        envHttpPort: "Port web HTTP exposé sur la machine hôte.",
        envHttpsPort: "Port web SSL exposé sur la machine hôte.",
        envMysqlPort: "Port MariaDB accessible depuis l'extérieur.",
        envAdminUser: "Identifiant de connexion administrateur au panel.",
        envAdminPassVal: "généré",
        envAdminPass: "Mot de passe de l'administrateur principal.",
        envDbName: "Nom de la base de données interne.",
        faqTitle: "FAQ & Commandes Utiles",
        faqQ1: "Comment consulter les logs en temps réel ?",
        faqA1: "Exécutez : <code>docker compose logs -f</code>.",
        faqQ2: "Comment changer le port sans réinstaller ?",
        faqA2: "Modifiez <code>ALTERNC_HTTP_PORT</code> dans votre fichier <code>.env</code>, puis lancez : <code>docker compose up -d</code>.",
        tocTitle: "Sur cette page"
      },
      en: {
        docTitle: "AlternC Documentation | Free & Self-Managed Platform",
        brandBadge: "Self-Management & Commons",
        searchPlaceholder: "Search documentation...",
        sidebarGroup1: "Getting Started & Foundations",
        sidebarGroup2: "Architecture & Deployment",
        navIntro: "Introduction",
        navEthics: "Ethics & Anti-Capitalism",
        navDocker: "Docker Installation",
        navPorts: "Port Isolation",
        navUI: "UI & Design System 2026",
        navProxy: "Nginx & Reverse Proxy",
        navEnv: "Environment Variables",
        navFaq: "FAQ & Troubleshooting",
        introTitle: "AlternC Documentation",
        introLead: "Emancipatory, self-managed free hosting platform, powered by PHP 8.3 and MariaDB in isolated containers with zero port conflicts.",
        featEthicsTitle: "Self-Management & Commons",
        featEthicsDesc: "Emancipation from Big Tech, copyleft free software, and horizontal infrastructure governance.",
        featDockerTitle: "Docker PHP 8.3",
        featDockerDesc: "Modern container stack running PHP 8.3, MariaDB 10.11 LTS, and strict volume data persistence.",
        featPortsTitle: "Zero Port Conflicts",
        featPortsDesc: "Isolated HTTP (8080), SSL (8443), and DB (3307) ports. Never blocks existing host services.",
        featSpotlightTitle: "Navigation & Spotlight",
        featSpotlightDesc: "Command palette (Ctrl+K), sober dark/light modes, and dynamic interactive sync.",
        ethicsTitle: "Anti-Capitalist Ethics & Digital Commons",
        ethicsLead: "AlternC stands as a grassroots collective defense against commercial lock-ins and surveillance capitalism monopolies.",
        ethicsCard1Title: "Rejection of Big Tech & Enclosures",
        ethicsCard1Desc: "Active resistance against proprietary monopolies (AWS, Google Cloud, Azure) privatizing the web and harvesting user data. AlternC grants full autonomy.",
        ethicsCard2Title: "Popular Self-Management",
        ethicsCard2Desc: "Horizontal governance, collective resource management, and direct technical sovereignty without middlemen or corporate tutelage.",
        ethicsCard3Title: "Digital Commons Defense",
        ethicsCard3Desc: "100% free software under copyleft (GPLv2+), open protocols, zero external CDNs, and zero telemetry or tracking.",
        ethicsCard4Title: "Frugality & Emancipatory Sobriety",
        ethicsCard4Desc: "Lightweight architecture running completely offline-first, respectful of hardware lifespans and ecological resources.",
        dockerTitle: "1-Command Docker Installation",
        dockerDesc: "A modern automated CLI script configures the environment, checks available host ports, and deploys the stack.",
        dockerHeader: "bash — Automated deployment",
        btnCopy: "Copy",
        btnCopied: "Copied!",
        dockerCalloutTitle: "Non-interactive deployment (CI/CD)",
        dockerCalloutDesc: "For automated unattended installations: <code>./install.sh -y</code>.",
        portsTitle: "Port Isolation",
        portsDesc: "The container architecture maps dedicated ports via .env to ensure peaceful coexistence with host services:",
        thService: "Service",
        thHostPort: "Default Host Port",
        thContainerPort: "Container Port",
        thEnvVar: "Environment Variable",
        serviceWebHttp: "Web HTTP",
        serviceWebHttps: "Web HTTPS (SSL)",
        serviceDb: "MariaDB / MySQL",
        uiTitle: "Modern 2026 Interface",
        uiDesc: "The control panel features a contemporary, responsive, and ergonomic dashboard:",
        uiPoint1: "<strong>Layout Architecture</strong>: Sticky sidebar with local SVG icons, top navbar with server status.",
        uiPoint2: "<strong>Dark & Light Modes</strong>: Instant theme toggling saved in <code>localStorage</code> without flash.",
        uiPoint3: "<strong>Tabular Data</strong>: Clean tables, subtle zebra striping, hover states, and high accessibility contrasts.",
        uiSpotlightTitle: "Command Palette (Ctrl+K)",
        uiSpotlightDesc: "Press Ctrl+K or Cmd+K on any page to open the fast Spotlight search modal.",
        proxyTitle: "Nginx Reverse Proxy Integration",
        proxyDesc: "To expose AlternC on a public subdomain using an Nginx reverse proxy:",
        proxyHeader: "nginx.conf — Reverse Proxy VirtualHost",
        envTitle: "Environment Variables Reference",
        thVar: "Variable",
        thDefault: "Default",
        thDesc: "Description",
        envHttpPort: "HTTP web port exposed on host machine.",
        envHttpsPort: "SSL HTTPS web port exposed on host machine.",
        envMysqlPort: "MariaDB database port accessible externally.",
        envAdminUser: "Primary admin username for control panel.",
        envAdminPassVal: "generated",
        envAdminPass: "Primary admin password.",
        envDbName: "Internal database name.",
        faqTitle: "FAQ & Useful Commands",
        faqQ1: "How to inspect live container logs?",
        faqA1: "Run: <code>docker compose logs -f</code>.",
        faqQ2: "How to change exposed ports without reinstalling?",
        faqA2: "Update <code>ALTERNC_HTTP_PORT</code> in your <code>.env</code> file, then run: <code>docker compose up -d</code>.",
        tocTitle: "On this page"
      },
      es: {
        docTitle: "Documentación de AlternC | Plataforma Libre y Autogestionada",
        brandBadge: "Autogestión y Comunes",
        searchPlaceholder: "Buscar en la documentación...",
        sidebarGroup1: "Inicio y Fundamentos",
        sidebarGroup2: "Arquitectura y Despliegue",
        navIntro: "Introducción",
        navEthics: "Ética y Anticapitalismo",
        navDocker: "Instalación con Docker",
        navPorts: "Aislamiento de Puertos",
        navUI: "Interfaz y Diseño 2026",
        navProxy: "Nginx y Proxy Inverso",
        navEnv: "Variables de Entorno",
        navFaq: "Preguntas Frecuentes",
        introTitle: "Documentación de AlternC",
        introLead: "Plataforma de alojamiento libre, emancipadora y autogestionada, impulsada por PHP 8.3 y MariaDB en contenedores aislados sin conflictos de puertos.",
        featEthicsTitle: "Autogestión y Comunes",
        featEthicsDesc: "Emancipación frente a las Big Tech, software libre copyleft y gobernanza horizontal de recursos.",
        featDockerTitle: "Docker PHP 8.3",
        featDockerDesc: "Contenedores modernos con PHP 8.3, MariaDB 10.11 LTS y persistencia estricta de volúmenes.",
        featPortsTitle: "Cero Conflictos de Puertos",
        featPortsDesc: "Puertos HTTP (8080), SSL (8443) y DB (3307) aislados sin interferir con servicios del anfitrión.",
        featSpotlightTitle: "Navegación y Spotlight",
        featSpotlightDesc: "Paleta de comandos (Ctrl+K), modos claro/oscuro sobrios y sincronización interactiva.",
        ethicsTitle: "Ética Anticapitalista y Bienes Comunes",
        ethicsLead: "AlternC surge y se mantiene como resistencia colectiva frente al capitalismo de vigilancia y sus monopolios privativos.",
        ethicsCard1Title: "Rechazo a las Big Tech y Cercamientos",
        ethicsCard1Desc: "Oposición frontal a los monopolios privativos (AWS, Google Cloud, Azure) que mercantilizan datos personales. AlternC garantiza plena autonomía.",
        ethicsCard2Title: "Autogestión Comunitaria",
        ethicsCard2Desc: "Control horizontal de servidores, correos y dominios sin tutelas corporativas ni intermediarios mercantiles.",
        ethicsCard3Title: "Defensa de los Comunes",
        ethicsCard3Desc: "Software 100% libre bajo copyleft (GPLv2+), estándares abiertos, cero CDN externas y cero rastreo.",
        ethicsCard4Title: "Frugalidad y Sobriedad",
        ethicsCard4Desc: "Arquitectura ligera que funciona de forma autónoma (offline-first), respetando los equipos y el entorno.",
        dockerTitle: "Instalación en 1 Comando con Docker",
        dockerDesc: "Un script moderno automatizado configura el entorno, comprueba puertos disponibles y levanta los servicios.",
        dockerHeader: "bash — Despliegue automatizado",
        btnCopy: "Copiar",
        btnCopied: "¡Copiado!",
        dockerCalloutTitle: "Despliegue no interactivo (CI/CD)",
        dockerCalloutDesc: "Para instalación desatendida: <code>./install.sh -y</code>.",
        portsTitle: "Aislamiento de Puertos",
        portsDesc: "La arquitectura Docker aísla cada puerto mediante el archivo .env para convivir con otros servicios:",
        thService: "Servicio",
        thHostPort: "Puerto Anfitrión Predeterminado",
        thContainerPort: "Puerto Contenedor",
        thEnvVar: "Variable de Entorno",
        serviceWebHttp: "Web HTTP",
        serviceWebHttps: "Web HTTPS (SSL)",
        serviceDb: "MariaDB / MySQL",
        uiTitle: "Interfaz y Diseño 2026",
        uiDesc: "El panel de control cuenta con un diseño contemporáneo, fluido y accesible:",
        uiPoint1: "<strong>Estructura Layout</strong>: Barra lateral fija con iconos SVG locales, barra superior con estado.",
        uiPoint2: "<strong>Modos Claro y Oscuro</strong>: Cambio inmediato almacenado en <code>localStorage</code> sin parpadeos.",
        uiPoint3: "<strong>Tablas de Datos</strong>: Filas espaciadas, contrastes contrastados y estados al pasar el ratón.",
        uiSpotlightTitle: "Paleta de Comandos (Ctrl+K)",
        uiSpotlightDesc: "Presione Ctrl+K o Cmd+K en cualquier pantalla para abrir la búsqueda rápida Spotlight.",
        proxyTitle: "Integración con Proxy Inverso (Nginx)",
        proxyDesc: "Para exponer AlternC en un subdominio público mediante Nginx:",
        proxyHeader: "nginx.conf — VirtualHost Proxy Inverso",
        envTitle: "Variables de Entorno .env",
        thVar: "Variable",
        thDefault: "Predeterminado",
        thDesc: "Descripción",
        envHttpPort: "Puerto HTTP expuesto en el anfitrión.",
        envHttpsPort: "Puerto SSL HTTPS expuesto en el anfitrión.",
        envMysqlPort: "Puerto MariaDB accesible exteriormente.",
        envAdminUser: "Usuario administrador principal.",
        envAdminPassVal: "generado",
        envAdminPass: "Contraseña del administrador principal.",
        envDbName: "Nombre de la base de datos interna.",
        faqTitle: "Preguntas Frecuentes y Comandos",
        faqQ1: "¿Cómo consultar los registros en directo?",
        faqA1: "Ejecute: <code>docker compose logs -f</code>.",
        faqQ2: "¿Cómo cambiar puertos sin reinstalar?",
        faqA2: "Modifique <code>ALTERNC_HTTP_PORT</code> en su archivo <code>.env</code> y ejecute: <code>docker compose up -d</code>.",
        tocTitle: "En esta página"
      }
    };

    /* Language Switcher Logic */
    function setLanguage(lang) {
      if (!translations[lang]) lang = 'eo';
      const dict = translations[lang];
      document.documentElement.setAttribute('lang', lang);
      localStorage.setItem('doc-lang', lang);

      // Update text content
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
          el.textContent = dict[key];
        }
      });

      // Update HTML content
      document.querySelectorAll('[data-i18n-html]').forEach(el => {
        const key = el.getAttribute('data-i18n-html');
        if (dict[key]) {
          el.innerHTML = dict[key];
        }
      });

      // Update placeholders
      document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key]) {
          el.setAttribute('placeholder', dict[key]);
        }
      });

      // Update buttons active class
      document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
      });

      // Update document title
      if (dict.docTitle) {
        document.title = dict.docTitle;
      }
    }

    // Attach click listeners to language buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const lang = btn.getAttribute('data-lang');
        setLanguage(lang);
      });
    });

    // Initial Language: stored or default to Esperanto
    const initialLang = localStorage.getItem('doc-lang') || 'eo';
    setLanguage(initialLang);

    /* Theme Toggle */
    const themeBtn = document.getElementById('theme-btn');
    const themeIcon = document.getElementById('theme-icon');

    const sunSvg = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
    const moonSvg = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';

    function updateTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('doc-theme', theme);
      themeIcon.innerHTML = theme === 'dark' ? sunSvg : moonSvg;
    }

    const savedTheme = localStorage.getItem('doc-theme') || 'dark';
    updateTheme(savedTheme);

    themeBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      updateTheme(current === 'dark' ? 'light' : 'dark');
    });

    /* Copy Code */
    function copyCode(btn) {
      const pre = btn.closest('.code-box').querySelector('pre');
      navigator.clipboard.writeText(pre.innerText).then(() => {
        const lang = document.documentElement.getAttribute('lang') || 'eo';
        const copiedText = (translations[lang] && translations[lang].btnCopied) || 'OK!';
        const original = btn.innerText;
        btn.innerText = copiedText;
        setTimeout(() => { btn.innerText = original; }, 2000);
      });
    }

    /* Search Filter */
    const searchInput = document.getElementById('doc-search');
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase();
      document.querySelectorAll('.sidebar-link').forEach(link => {
        const text = link.textContent.toLowerCase();
        link.parentElement.style.display = text.includes(q) ? 'block' : 'none';
      });
    });

    /* Active Scrollspy */
    function setActiveSection(id) {
      if (!id) return;
      document.querySelectorAll('.sidebar-link').forEach(link => {
        const href = link.getAttribute('href');
        link.classList.toggle('active', href === '#' + id);
      });
      document.querySelectorAll('.toc-link').forEach(link => {
        const href = link.getAttribute('href');
        link.classList.toggle('active', href === '#' + id);
      });
    }

    document.querySelectorAll('.sidebar-link, .toc-link').forEach(link => {
      link.addEventListener('click', () => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
          setActiveSection(href.substring(1));
        }
      });
    });

    const sections = Array.from(document.querySelectorAll('section[id]'));
    function updateOnScroll() {
      const scrollPos = window.scrollY + 120;
      let currentSection = sections[0] ? sections[0].id : null;
      for (const sec of sections) {
        if (sec.offsetTop <= scrollPos) {
          currentSection = sec.id;
        }
      }
      if (currentSection) {
        setActiveSection(currentSection);
      }
    }

    window.addEventListener('scroll', updateOnScroll, { passive: true });
    updateOnScroll();
  </script>
</body>
</html>
"""

with open("/home/anar/Bureau/AlternC/docs/index.html", "w", encoding="utf-8") as f:
    f.write(html_template.strip() + "\n")

print("Generated docs/index.html successfully with 4 languages (eo, fr, en, es)")

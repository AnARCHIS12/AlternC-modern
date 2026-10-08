<?php
/*
 ----------------------------------------------------------------------
 LICENSE

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License (GPL)
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 To read the license please visit http://www.gnu.org/copyleft/gpl.html
 ----------------------------------------------------------------------
*/

/**
 * main HEADER of all HTML page of the panel
 * 
 * @copyright AlternC-Team 2000-2017 https://alternc.com/ 
 */

if (!isset($charset) || ! $charset) $charset="UTF-8";
@header("Content-Type: text/html; charset=$charset");

require_once("html-head.php");
?>
<body>
<div id="global" class="app-layout clearfix">
<aside id="menu" class="app-sidebar"><?php include_once("menu.php"); ?></aside>
<div class="app-main-area">
  <header class="app-topbar">
    <div class="topbar-left">
      <button type="button" id="sidebar-toggle" class="topbar-btn" title="<?php __("Toggle Menu"); ?>" aria-label="Menu">
        <i class="fas fa-bars"></i>
      </button>
      <div class="topbar-title">
        <span class="server-pill"><i class="fas fa-server"></i> <?php echo htmlspecialchars(!empty($_SERVER['HTTP_HOST']) ? $_SERVER['HTTP_HOST'] : 'AlternC'); ?></span>
      </div>
    </div>

    <div class="topbar-center">
      <div class="topbar-search">
        <i class="fas fa-search search-icon"></i>
        <input type="text" id="menu-quicksearch" placeholder="<?php __("Quick search... (Ctrl+K)"); ?>" autocomplete="off" />
        <kbd class="search-kbd">Ctrl K</kbd>
      </div>
    </div>

    <div class="topbar-right">
      <button type="button" id="theme-toggle" class="topbar-btn" title="<?php __("Toggle Dark / Light Theme"); ?>" aria-label="Theme">
        <i class="fas fa-moon" id="theme-icon"></i>
      </button>
      <div class="topbar-user">
        <a href="mem_param.php" class="user-link" title="<?php __("My Account"); ?>">
          <span class="user-avatar"><i class="fas fa-user"></i></span>
          <span class="user-name"><?php echo htmlspecialchars(isset($mem->user['login']) ? $mem->user['login'] : ''); ?></span>
        </a>
        <a href="mem_logout.php" class="logout-btn" title="<?php __("Logout"); ?>">
          <i class="fas fa-sign-out-alt"></i>
        </a>
      </div>
    </div>
  </header>

  <!-- Quick search Spotlight modal -->
  <div id="quicksearch-modal" class="quicksearch-overlay" style="display:none;">
    <div class="quicksearch-box">
      <div class="quicksearch-header">
        <i class="fas fa-search"></i>
        <input type="text" id="quicksearch-input" placeholder="<?php __("Search domain, mail, database, quota..."); ?>" />
        <button type="button" class="quicksearch-close" id="quicksearch-close">&times;</button>
      </div>
      <div class="quicksearch-results" id="quicksearch-results"></div>
    </div>
  </div>

  <div id="content" class="app-content">
<?php

if ($isinvited && isset($oldid) && !empty($oldid) && $oldid!=$cuid ) {
  echo "<div class='alert alert-warning'>";
  echo "<i class='fas fa-exclamation-triangle'></i> ";
  __("Administrator session. you may <a href='adm_login.php'>return to your account</a> or <a href='adm_cancel.php'>cancel this feature</a>.");
  if ($oldid == 2000) echo ' '._("You can also <a href='adm_update_domains.php'>apply changes</a>."); // Yes, hardcoded uid. We will rewrite permissions another day
  echo "</div>";
}
if ( panel_islocked() ) {
  echo "<div class='alert alert-danger'>";
  echo "<i class='fas fa-lock'></i> ";
  __("Panel is locked! No one can login!");
  echo "</div>";
}
?>

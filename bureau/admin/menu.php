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
 * Main left menu of AlternC, uses Hooks 
 * 
 * @copyright AlternC-Team 2000-2017 https://alternc.com/
 */

require_once("../class/config.php");

// Getting logo
$logo = variable_get('logo_menu', '' ,'You can specify a logo for the menu, example /images/my_logo.png .', array('desc'=>'URL','type'=>'string'));

echo '<div class="menutoplogo">';
if (!empty($logo) && !is_null($logo)) {
  echo "<img src=\"".$logo."\" border='0' alt='AlternC' />";
} else {
  echo "<img src='images/logo3.png' border='0' alt='AlternC' />";
}
echo '<div class="sidebar-brand-text">';
echo '<span class="sidebar-brand-title">AlternC</span>';
echo '<span class="sidebar-brand-sub">' . _("Cloud Panel") . '</span>';
echo '</div>';
echo "</div>";
?>

<div class="currentuser">
  <span><?php echo sprintf(_("Welcome %s"), htmlspecialchars($mem->user["login"])); ?></span>
</div>

<?php

$category_icons = array(
  'dom' => 'fa-globe',
  'mail' => 'fa-envelope',
  'mysql' => 'fa-database',
  'ftp' => 'fa-folder-open',
  'bro' => 'fa-file-code',
  'quota' => 'fa-chart-pie',
  'cron' => 'fa-clock',
  'log' => 'fa-list-alt',
  'hta' => 'fa-shield-alt',
  'admin' => 'fa-user-shield',
  'authip' => 'fa-network-wired',
  'mem' => 'fa-user-cog',
  'piwik' => 'fa-chart-line',
  'stats' => 'fa-chart-bar',
  'lxc' => 'fa-cube',
  'vm' => 'fa-server',
);

$obj_menu = $menu->getmenu();

foreach ($obj_menu as $k => $m ) {
  $icon_class = isset($category_icons[$k]) ? $category_icons[$k] : 'fa-folder';

  echo "<div class='menu-box {$k}-menu ".(!empty($m['divclass'])?$m['divclass']:'')."'>\n";
  echo "  <a href=\"".$m['link']."\"";
  if (!empty($m['target'])) echo " target='". $m['target']."' ";
  echo ">\n";
  echo "    <div class='menu-title'>\n";
  echo "      <div class='menu-title-left'>\n";
  echo "        <span class='menu-icon'><i class='fas {$icon_class}'></i></span>\n";
  echo "        <span class='menu-text " . (!empty($m['class']) ? $m['class'] : '') . "'>" . $m['title'] . "</span>\n";
  echo "      </div>\n";

  if (isset($m['quota_total'])) {
    $is_full = !$quota->cancreate($k);
    echo "      <span class='quota-badge" . ($is_full ? ' quota-badge-full' : '') . "'>" . $m['quota_used'] . "/" . $m['quota_total'] . "</span>\n";
  }
  echo "    </div>\n";
  echo "  </a>\n";

  if (!empty($m['links'])) {
    if ($m['visibility']) $visible = ""; else $visible = "style=\"display: none\"";
    echo "<div class='menu-content' id='menu-$k' $visible >";
    echo "  <ul>";
    foreach ($m['links'] as $l) {
      if ($l['txt'] == 'progressbar') {
        $usage_percent = (int) ($l['used'] / $l['total'] * 100);
        echo "<li class='menu-progress-item'>";
        echo '<div class="progress-bar-container">';
        echo '<div class="progress-bar-track"><div class="progress-bar-fill" style="width:'.$usage_percent.'%; background-color:'.PercentToColor($usage_percent).'" ></div></div>';
        echo '<span class="progress-bar-label">'.$usage_percent.'%</span>';
        echo '</div>';
        echo "</li>";
        continue;
      }
      echo "<li><a href=\"".$l['url']."\" ";
      if (!empty($l['onclick'])) echo " onclick='". $l['onclick']."' ";
      if (!empty($l['target'])) echo " target='". $l['target']."' ";
      echo " ><span class='".(empty($l['class'])?'':$l['class'])."'>";
      if (!empty($l['ico'])) echo "<img src='".$l['ico']."' alt='' />&nbsp;";
      echo $l['txt'];
      echo "</span></a></li>";
    }
    echo "  </ul>";
    echo "</div>";
  }
  echo "</div>";
}
?>

<div class="sidebar-footer">
  <a href="about.php" title="<?php __("About"); ?>">AlternC <?php echo "$L_VERSION"; ?></a>
</div>

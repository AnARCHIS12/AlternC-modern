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
 * Show the login page (hence the config_nochk below)
 * this page is the only one, with logout.php, to NOT ask 
 * for authentication 
 *
 * @copyright AlternC-Team 2000-2017 https://alternc.com/ 
 */

require_once("../class/config_nochk.php");

if ($mem->checkid(false)) {
	Header("Location: /main.php");
	exit;
}

$mem->del_session();

$H=getenv("HTTP_HOST");

if (!isset($restrictip)) {
  $restrictip=1;
}
if (!isset($charset) || ! $charset) $charset="UTF-8";
@header("Content-Type: text/html; charset=$charset");

require_once("html-head.php");
?>
<body class="login_page">
  <div class="login-wrapper">
    <div class="login-top-bar">
      <button id="theme-toggle-btn" class="theme-toggle-pill" type="button" onclick="toggleTheme()" aria-label="<?php echo _("Toggle theme"); ?>">
        <i id="theme-icon" class="fas fa-moon"></i>
      </button>
    </div>

    <div id="content" class="login-card">
<?php
// Getting logo
$logo = variable_get('logo_login', '' ,'You can specify a logo for the login page, example /images/my_logo.png .', array('desc'=>'URL','type'=>'string'));
if ( empty($logo) || ! $logo ) { 
  $logo = 'images/logo.png'; 
}
?>
      <div class="login-header">
        <div class="login-logo-box">
          <img src="<?php echo $logo; ?>" alt="AlternC" class="login-logo-img" />
        </div>
        <h1 class="login-main-title"><?php __("AlternC access"); ?></h1>
        <p class="login-desc"><?php __("To connect to the hosting control panel, enter your AlternC's login and password in the following form and click 'Enter'"); ?></p>
      </div>

      <?php echo $msg->msg_html_all(); ?>

      <?php
      if (isset($_GET['authip_token'])) $authip_token=$_GET['authip_token'];
      if (variable_get('https_warning', false, 'warn users to switch to HTTPS') && !isset($_SERVER['HTTPS'])) {
        echo '<div class="unsecure"><strong>' . sprintf(_('WARNING: you are trying to access the control panel insecurely, click <a href="https://%s">here</a> to go to secure mode'), $_SERVER["HTTP_HOST"]) . '</strong></div>';
      }
      if (!empty($authip_token)) {
        echo "<div class='alert alert-warning'>" . _("You are attemping to connect without IP restriction.") . "</div>";
      }
      ?>

      <form action="login.php" method="post" name="loginform" class="login-form" target="_top">
        <?php csrf_get(); ?>
        <div class="form-field">
          <label for="username"><?php echo _("Username"); ?></label>
          <input type="text" class="int form-input" name="username" id="username" value="" maxlength="128" autocapitalize="none" autocomplete="username" placeholder="<?php echo _("Username"); ?>" required />
        </div>

        <div class="form-field">
          <label for="password"><?php echo _("Password"); ?></label>
          <input type="password" class="int form-input" name="password" id="password" value="" maxlength="128" autocomplete="current-password" placeholder="<?php echo _("Password"); ?>" required />
        </div>

        <div class="form-submit-row">
          <input type="submit" class="inb btn-login-submit" name="submit" onclick='return logmein();' value="<?php __("Enter"); ?>" />
          <input type="hidden" id="restrictip" name="restrictip" value="0" />
          <input type="hidden" id="authip_token" name="authip_token" value="<?php ehe( (empty($authip_token)?'':$authip_token) ) ?>" />
        </div>
      </form>

      <div class="login-footer">
        <div class="login-links-row">
          <a href="request_reset.php" class="login-reset-link"><?php echo _('Request new password'); ?></a>
        </div>

        <div class="login-lang-box">
          <div class="login-lang-label"><?php echo _("If you want to use a different language, choose it in the list below"); ?></div>
          <div class="login-lang-pills">
            <?php foreach($locales as $l): ?>
              <?php $isActive = ($l === $lang); ?>
              <a href="?setlang=<?php echo urlencode($l); ?>" class="lang-pill <?php echo $isActive ? 'active' : ''; ?>">
                <?php echo htmlspecialchars(isset($lang_translation[$l]) ? $lang_translation[$l] : $l); ?>
              </a>
            <?php endforeach; ?>
          </div>
        </div>

        <div class="login-cookie-hint">
          <span><?php __("You must accept the session cookie to log-in"); ?></span>
        </div>

        <?php
          $res=$hooks->invoke("hook_admin_webmail");
          if (($wr=variable_get("webmail_redirect")) && isset($res[$wr]) && $res[$wr]) {
            $url=$res[$wr];
          } else {
            foreach($res as $r) if ($r!==false) { $url=$r; break; }
          }
          if (isset($url) && $url) {
        ?>
          <div class="webmail-link-box">
            <a href="<?php echo $url; ?>"><?php __("To read your mail in a browser, click here to go to your server's Webmail"); ?></a>
          </div>
        <?php } ?>
      </div>

      <div class="alternc_powered">
        <a href="https://alternc.com/"><img src="images/powered_by_alternc2.png" width="128" height="32" alt="Powered by AlternC" /></a>
      </div>

    </div>
  </div>

  <script type="text/javascript">
  $('#username').focus();

  function logmein(){
    if ( $('#username').val() =='' || $('#password').val() =='' ) {
      alert("<?php __("Need a login and a password"); ?>");
      return false;
    }
    return true;
  }
  </script>
</body>
</html>

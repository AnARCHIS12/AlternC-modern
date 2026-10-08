<?php

$lang_translation = array(
    "en_US" => "English",
    "fr_FR" => "Français",
    "es_ES" => "Español",
    "de_DE" => "Deutsch",
);

global $arr_lang_translation;
$arr_lang_translation = $lang_translation;

function update_locale($langpath) {
    global $arr_lang_translation;
    $locales = array();
    foreach ($arr_lang_translation as $code => $label) {
        if (file_exists($langpath . '/' . $code)) {
            $locales[$code] = $code;
        }
    }
    if (!count($locales)) {
        $locales = array("en_US" => "en_US");
    }
    return $locales;
}

// setlang parameter or saved cookie
if (isset($_REQUEST["setlang"]) && !empty($_REQUEST["setlang"])) {
    $lang = trim($_REQUEST["setlang"]);
    $setlang = $lang;
} elseif (isset($_COOKIE['lang']) && !empty($_COOKIE['lang'])) {
    $lang = trim($_COOKIE['lang']);
}

$langpath = bindtextdomain("alternc", ALTERNC_LOCALES);
$locales = update_locale($langpath);

if (!isset($lang) || empty($lang) || !isset($locales[$lang])) {
    $pref = isset($_SERVER["HTTP_ACCEPT_LANGUAGE"]) ? strtolower(substr(trim($_SERVER["HTTP_ACCEPT_LANGUAGE"]), 0, 2)) : 'en';
    $lang = "en_US";
    foreach ($locales as $l) {
        if (strtolower(substr($l, 0, 2)) === $pref) {
            $lang = $l;
            break;
        }
    }
}

if (isset($setlang) && isset($lang)) {
    setcookie("lang", $lang, time() + (365 * 86400), "/");
    $_COOKIE['lang'] = $lang;
}

/* Language ok, set the locale environment */
$locale_utf8 = (strpos($lang, '.') === false) ? $lang . ".UTF-8" : $lang;
putenv("LC_ALL=" . $locale_utf8);
putenv("LC_MESSAGES=" . $locale_utf8);
putenv("LANG=" . $locale_utf8);
putenv("LANGUAGE=" . $locale_utf8);

setlocale(LC_ALL, $locale_utf8, $lang, str_replace('.UTF-8', '.utf8', $locale_utf8), 'C.UTF-8');

bindtextdomain("alternc", ALTERNC_LOCALES);
bind_textdomain_codeset("alternc", "UTF-8");
textdomain("alternc");

$charset = "UTF-8";

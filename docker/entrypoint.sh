#!/bin/bash
set -e

echo "[alternc-init] Initialisation de l'environnement..."

# Defaults
DB_HOST="${DB_HOST:-db}"
DB_NAME="${DB_NAME:-alternc}"
DB_USER="${DB_USER:-alternc}"
DB_PASS="${DB_PASS:-alternc_secret}"
ALTERNC_FQDN="${ALTERNC_FQDN:-localhost}"
ALTERNC_ADMIN_USER="${ALTERNC_ADMIN_USER:-admin}"
ALTERNC_ADMIN_PASS="${ALTERNC_ADMIN_PASS:-admin123456}"

# Ensure directories exist
mkdir -p /etc/alternc/templates/apache2 \
         /var/lib/alternc/panel \
         /var/lib/alternc/apache-vhost/manual \
         /var/log/alternc \
         /var/alternc/html \
         /var/alternc/mail \
         /run/alternc

# Generate /etc/alternc/my.cnf
cat <<EOF > /etc/alternc/my.cnf
[client]
user = ${DB_USER}
password = ${DB_PASS}
host = ${DB_HOST}
database = ${DB_NAME}
ssl = 0
EOF
chmod 640 /etc/alternc/my.cnf

# Generate /etc/alternc/local.sh
cat <<EOF > /etc/alternc/local.sh
FQDN="${ALTERNC_FQDN}"
NS1_HOSTNAME="ns1.${ALTERNC_FQDN}"
NS2_HOSTNAME="ns2.${ALTERNC_FQDN}"
DEFAULT_MX="mail.${ALTERNC_FQDN}"
ALTERNC_MAIL="/var/alternc/mail"
ALTERNC_HTML="/var/alternc/html"
ALTERNC_LOGS="/var/log/alternc"
MYSQL_HOST="${DB_HOST}"
MYSQL_DATABASE="${DB_NAME}"
MYSQL_USER="${DB_USER}"
MYSQL_PASS="${DB_PASS}"
MYSQL_CLIENT="%"
EOF
chmod 640 /etc/alternc/local.sh

# Wait for MariaDB
echo "[alternc-init] En attente de la base de données MariaDB (${DB_HOST}:3306)..."
max_tries=30
count=0
until php -r "
  try {
    \$pdo = new PDO('mysql:host=${DB_HOST};dbname=${DB_NAME}', '${DB_USER}', '${DB_PASS}');
    exit(0);
  } catch (Exception \$e) {
    exit(1);
  }
" >/dev/null 2>&1; do
  count=$((count+1))
  if [ $count -ge $max_tries ]; then
    echo "[alternc-error] Impossible de se connecter a la base de donnees apres ${max_tries} tentatives."
    exit 1
  fi
  sleep 2
done
echo "[alternc-init] Connexion MariaDB etablie avec succes."

# Initialize DB schema if table 'membres' does not exist
TABLE_EXISTS=$(php -r "
  \$pdo = new PDO('mysql:host=${DB_HOST};dbname=${DB_NAME}', '${DB_USER}', '${DB_PASS}');
  \$stmt = \$pdo->query(\"SHOW TABLES LIKE 'membres'\");
  echo \$stmt->rowCount();
")

if [ "$TABLE_EXISTS" -eq "0" ]; then
  echo "[alternc-init] Initialisation des tables AlternC (mysql.sql)..."
  if [ -f /usr/share/alternc/install/mysql.sql ]; then
    mariadb --skip-ssl -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASS}" "${DB_NAME}" < /usr/share/alternc/install/mysql.sql
    echo "[alternc-init] Schema de base de donnees cree."
  fi
else
  echo "[alternc-init] Base de donnees deja initialisee."
fi

# Ensure user permissions on MariaDB for database management
if [ -n "${DB_ROOT_PASS}" ]; then
  mariadb --skip-ssl -h "${DB_HOST}" -u root -p"${DB_ROOT_PASS}" -e "GRANT ALL PRIVILEGES ON *.* TO '${DB_USER}'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;" 2>/dev/null || true
fi

# Create default admin account if not already present
ADMIN_EXISTS=$(php -r "
  \$pdo = new PDO('mysql:host=${DB_HOST};dbname=${DB_NAME}', '${DB_USER}', '${DB_PASS}');
  \$stmt = \$pdo->prepare('SELECT COUNT(*) FROM membres WHERE login = ?');
  \$stmt->execute(['${ALTERNC_ADMIN_USER}']);
  echo \$stmt->fetchColumn();
" 2>/dev/null || echo "0")

if [ "$ADMIN_EXISTS" -eq "0" ]; then
  echo "[alternc-init] Creation du compte administrateur '${ALTERNC_ADMIN_USER}'..."
  php -r "
    require('/usr/share/alternc/panel/class/config_nochk.php');
    \$admin->enabled = 1;
    \$dbs = 1;
    \$db->query('SELECT MIN(id) AS id FROM db_servers;');
    if (\$db->next_record() && intval(\$db->Record['id'])) {
      \$dbs = \$db->Record['id'];
    } else {
      \$db->query(\"INSERT INTO db_servers SET name='Default', host='${DB_HOST}', login='${DB_USER}', password='${DB_PASS}', client='%';\");
      \$dbs = \$db->lastid();
    }
    \$admin->add_mem('${ALTERNC_ADMIN_USER}', '${ALTERNC_ADMIN_PASS}', 'Administrateur', 'Admin', 'admin@alternc.local', 1, 'default', 0, '', 0, '', \$dbs);
    \$db->query(\"UPDATE membres SET su=1 WHERE login='${ALTERNC_ADMIN_USER}';\");
    echo '[alternc-init] Compte admin initialise avec succes.\n';
  " || true
fi

# Ensure https_warning is disabled for local and port-forwarded HTTP panels
php -r "
  require('/usr/share/alternc/panel/class/config_nochk.php');
  variable_set('https_warning', 0);
" 2>/dev/null || true

# Compile gettext catalogs if not yet present
find /usr/share/alternc/panel/locales -maxdepth 1 -mindepth 1 -type d -name "*_*" | while read d; do
  if [ -d "$d/LC_MESSAGES" ] && [ ! -f "$d/LC_MESSAGES/alternc.mo" ]; then
    (
      cd "$d/LC_MESSAGES"
      if ls *.po 1> /dev/null 2>&1; then
        msgcat --use-first *.po > alternc.po 2>/dev/null || cat *.po > alternc.po
        msgfmt alternc.po -o alternc.mo 2>/dev/null || true
      fi
    )
  fi
done

# Ensure web server permissions
chown -R www-data:www-data /var/alternc /var/log/alternc /run/alternc /var/lib/alternc
chown www-data:www-data /etc/alternc/my.cnf /etc/alternc/local.sh

echo "[alternc-init] Demarrage du serveur web..."
exec "$@"

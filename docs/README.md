# AlternC — Documentation Technique (2026 Edition)

Bienvenue dans la documentation d'AlternC modernisé, conteneurisé sous Docker et équipé d'un Design System 2026.

## Sommaire
- [1. Vue d'ensemble & Architecture](#1-vue-densemble--architecture)
- [2. Installation rapide (Docker)](#2-installation-rapide-docker)
- [3. Séparation et isolation des ports](#3-séparation-et-isolation-des-ports)
- [4. Interface & Design System (2026)](#4-interface--design-system-2026)
- [5. Intégration Reverse Proxy](#5-intégration-reverse-proxy)
- [6. Variables d'environnement (.env)](#6-variables-denvironnement-env)
- [7. Commandes usuelles](#7-commandes-usuelles)

---

## 1. Vue d'ensemble & Architecture

AlternC est historiquement un panneau de contrôle pour serveurs Debian gérant :
- Serveur Web (Apache, PHP)
- Serveur Mail (Postfix, Dovecot)
- Serveur DNS (Bind9)
- Bases de données (MariaDB/MySQL, PhpMyAdmin)
- Utilisateurs FTP et quotas systèmes

Cette édition modernisée apporte :
1. **Conteneurisation Docker complète** (PHP 8.3 + MariaDB 10.11 LTS).
2. **Isolation des ports** : fini la monopolisation des ports 80, 443 et 3306 de l'hôte.
3. **Nouveau front-end SaaS (2026)** : Dark/Light mode automatique, design épuré, navigation fluide, palette de commande <kbd>Ctrl+K</kbd>.
4. **Script d'installation CLI moderne** ([install.sh](../install.sh)) avec détection dynamique des ports libres.

---

## 2. Installation rapide (Docker)

```bash
chmod +x install.sh
./install.sh
```

Pour un déploiement silencieux (CI/CD) :
```bash
./install.sh -y
```

Le script :
1. Vérifie la présence de Docker Engine et Docker Compose.
2. Détecte si les ports 8080, 8443 ou 3307 sont déjà pris sur votre machine hôte, et propose automatiquement les ports libres suivants.
3. Génère un fichier `.env` sécurisé avec des mots de passe aléatoires forts.
4. Construit l'image et démarre les services.
5. Valide que le panel répond correctement en HTTP.

---

## 3. Séparation et isolation des ports

Tous les ports sont configurables dans le fichier `.env` :

| Service | Port Hôte par défaut | Port Conteneur | Variable `.env` |
|---|---|---|---|
| **Web HTTP** | `8080` | `80` | `ALTERNC_HTTP_PORT` |
| **Web HTTPS** | `8443` | `443` | `ALTERNC_HTTPS_PORT` |
| **MariaDB** | `3307` | `3306` | `ALTERNC_MYSQL_PORT` |

Si vous possédez déjà un serveur Nginx, Traefik, ou un serveur de base de données sur votre machine, **aucun conflit ne survient**.

---

## 4. Interface & Design System (2026)

L'interface a été entièrement modernisée :
- **Doctype HTML5** et balise `<meta name="viewport">` pour une compatibilité mobile et tablette totale.
- **Thème sombre & clair** persistant (`localStorage`), sans scintillement au chargement.
- **Sidebar rétractable** avec icônes FontAwesome vectorielles et jauges de quotas animées.
- **Palette de commande "Spotlight"** : accessible avec <kbd>Ctrl+K</kbd> ou <kbd>Cmd+K</kbd> pour naviguer instantanément dans les sections, domaines et boîtes mail.
- Feuille de styles personnalisée chargée automatiquement dans `bureau/admin/styles/style-custom.css`.

---

## 5. Intégration Reverse Proxy

Pour router votre nom de domaine (ex: `panel.mondomaine.com`) vers AlternC :

### Nginx
```nginx
server {
    listen 80;
    server_name panel.mondomaine.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Caddy
```caddy
panel.mondomaine.com {
    reverse_proxy 127.0.0.1:8080
}
```

---

## 6. Variables d'environnement (.env)

```dotenv
ALTERNC_HTTP_PORT=8080
ALTERNC_HTTPS_PORT=8443
ALTERNC_MYSQL_PORT=3307
ALTERNC_BIND_IP=0.0.0.0
ALTERNC_DB_BIND_IP=127.0.0.1
ALTERNC_FQDN=localhost
ALTERNC_ADMIN_USER=admin
ALTERNC_ADMIN_PASS=votre_mot_de_passe
DB_NAME=alternc
DB_USER=alternc
DB_PASS=secret_db_pass
DB_ROOT_PASS=secret_root_pass
```

---

## 7. Commandes usuelles

* **Suivre les logs en direct** :
  ```bash
  docker compose logs -f
  ```
* **Arrêter le panneau** :
  ```bash
  docker compose stop
  ```
* **Redémarrer le panneau** :
  ```bash
  docker compose restart
  ```
* **Mettre à jour ou recompiler** :
  ```bash
  docker compose up -d --build
  ```

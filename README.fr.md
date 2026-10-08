<p align="center">
  <img src="bureau/admin/images/logo.png" alt="AlternC" width="300" />
</p>

# AlternC

> La plateforme libre, émancipatrice et autogérée d'hébergement web et mail, intégralement modernisée avec Docker, PHP 8.3 et MariaDB.

<div align="center">

**Lingvoj / Languages:** [Esperanto](README.md) • [Français](README.fr.md) • [English](README.en.md) • [Español](README.es.md)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.5%20Modern-2563eb?style=flat-square" alt="Version" />
  <img src="https://img.shields.io/badge/PHP-8.3%20Actif-10b981?style=flat-square" alt="PHP 8.3" />
  <img src="https://img.shields.io/badge/Conteneur-Docker%20Compose-059669?style=flat-square" alt="Docker Compose" />
  <img src="https://img.shields.io/badge/MariaDB-10.11%20LTS-0284c7?style=flat-square" alt="MariaDB 10.11" />
  <img src="https://img.shields.io/badge/CDN-0%25%20(Autonome)-0d9488?style=flat-square" alt="Sans-CDN" />
  <img src="https://img.shields.io/badge/%C3%89thique-Anticapitalisme%20%26%20Autogestion-7c3aed?style=flat-square" alt="Autogestion" />
  <img src="https://img.shields.io/badge/Emoji-0%25%20(Pro)-6366f1?style=flat-square" alt="Sans-Emoji" />
  <img src="https://img.shields.io/badge/Licence-GPL--2.0%2B-64748b?style=flat-square" alt="GPLv2+" />
</p>

---

## Présentation

**AlternC** est une suite logicielle libre historique dont l'objectif est de permettre aux collectifs, associations et personnes d'administrer leurs propres services web (sites, messagerie, comptes FTP, bases de données, domaines et DNS).

Conçue pour répondre aux impératifs d'aujourd'hui, cette version modernisée abandonne les méthodes de déploiement obsolètes au profit d'une conteneurisation légère, étanche et sécurisée sous **Docker et Docker Compose**, propulsée par **PHP 8.3** et **MariaDB 10.11 LTS**.

### Éthique Anticapitaliste & Communs Numériques

* **Refus de la Big Tech & des enclosures marchandes** : Résistance active face aux géants du cloud propriétaire (AWS, Google Cloud, Microsoft Azure) et au capitalisme de surveillance qui confisquent les données.
* **Autogestion et réappropriation populaire** : Reprise en main directe et horizontale de nos serveurs, sans dépendance mercantile ni tutelle d'entreprise.
* **Biens communs numériques** : Logiciel 100% libre (GPLv2+), protocoles décentralisés ouverts, zéro CDN externe et zéro télémétrie.

---

## Démarrage Rapide (1 Commande)

L'installation ne passe plus par d'anciens paquets système ; elle s'effectue en une seule commande via le script d'installation automatisé ou via Docker Compose :

```bash
# 1. Cloner le dépôt
git clone git@github.com:AnARCHIS12/AlternC-modern.git
cd AlternC-modern

# 2. Lancer l'installation automatisée (détection des ports libres)
chmod +x install.sh
./install.sh
```

Pour un déploiement automatisé sans interaction (ex. CI/CD) :

```bash
./install.sh -y
```

### Déploiement direct avec Docker Compose

```bash
# Copier le fichier d'environnement modèle
cp .env.example .env

# Démarrer les conteneurs en arrière-plan
docker compose up -d
```

L'interface d'administration est alors disponible sur `http://localhost:8080` (ou le port configuré).

---

## Architecture & Isolation des Ports

Afin de cohabiter harmonieusement avec d'autres services hébergés sur la même machine, chaque port exposé est isolé et entièrement paramétrable dans le fichier `.env` :

| Service | Port Hôte par défaut | Port Conteneur | Variable d'environnement |
| :--- | :--- | :--- | :--- |
| **Web (HTTP)** | `8080` | `80` | `ALTERNC_HTTP_PORT` |
| **Web (HTTPS/SSL)** | `8443` | `443` | `ALTERNC_HTTPS_PORT` |
| **MariaDB** | `3307` | `3306` | `ALTERNC_MYSQL_PORT` |

---

## Interface Contemporaine 2026

* **Design épuré et adaptatif** : Navigation latérale structurée avec icônes SVG locales et barre supérieure dynamique.
* **Thèmes sombre et clair** : Bascule instantanée mémorisée dans `localStorage` sans scintillement.
* **Recherche Spotlight (Ctrl+K)** : Palette de commande instantanée pour accéder rapidement à un domaine ou un outil.
* **Zéro CDN externe** : Toutes les polices système et composants sont hébergés localement (offline-first).

---

## Arborescence du Projet

```text
.
├── Dockerfile             # Image conteneur sous PHP 8.3 Apache
├── docker-compose.yml     # Orchestration des services Web et MariaDB 10.11
├── install.sh             # Script d'installation moderne avec détection de ports
├── .env.example           # Gabarit de configuration des ports et identifiants
├── bureau/                # Panneau de contrôle web en PHP
│   ├── admin/             # Vues et contrôleurs récents
│   └── class/             # Classes métier et abstractions
├── docs/                  # Portail de documentation autonome (0% CDN)
│   └── index.html         # Guide complet avec recherche locale et thèmes
└── README.md              # Documentation principale d'accueil en espéranto
```

---

## Contribution & Licence

Les contributions de la communauté sont les bienvenues dans le respect de l'éthique du logiciel libre, du langage inclusif et de l'émancipation collective.

* **Licence** : GNU General Public License v2 ou ultérieure (GPL-2.0-or-later). Voir [COPYING](COPYING).

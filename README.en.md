# AlternC

> Emancipatory, self-managed, and anti-capitalist free software suite for web and email hosting, fully modernized with Docker, PHP 8.3, and MariaDB.

<div align="center">

**Lingvoj / Languages:** [Esperanto](README.md) • [Français](README.fr.md) • [English](README.en.md) • [Español](README.es.md)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.5%20Modern-2563eb?style=flat-square" alt="Version" />
  <img src="https://img.shields.io/badge/PHP-8.3%20Active-10b981?style=flat-square" alt="PHP 8.3" />
  <img src="https://img.shields.io/badge/Container-Docker%20Compose-059669?style=flat-square" alt="Docker Compose" />
  <img src="https://img.shields.io/badge/MariaDB-10.11%20LTS-0284c7?style=flat-square" alt="MariaDB 10.11" />
  <img src="https://img.shields.io/badge/CDN-0%25%20(Autonomous)-0d9488?style=flat-square" alt="Offline-First" />
  <img src="https://img.shields.io/badge/Ethics-Self--Management%20%26%20Anti--Capitalist-7c3aed?style=flat-square" alt="Self-Management" />
  <img src="https://img.shields.io/badge/Emojis-0%25%20(Pro)-6366f1?style=flat-square" alt="Zero Emoji" />
  <img src="https://img.shields.io/badge/License-GPL--2.0%2B-64748b?style=flat-square" alt="GPLv2+" />
</p>

---

## Overview

**AlternC** is an established free software hosting management platform designed to empower collectives, non-profits, and individuals to maintain direct, self-managed control over their internet services (web servers, email mailboxes, FTP accounts, databases, and DNS zones).

Re-engineered for contemporary operational requirements, AlternC discards legacy system packaging in favor of an isolated, secure deployment using **Docker and Docker Compose**, powered by **PHP 8.3** and **MariaDB 10.11 LTS**.

### Anti-Capitalist Ethics & Digital Commons

* **Rejection of Big Tech & commercial cloud lock-in**: Active resistance against surveillance capitalism and proprietary cloud monopolies (AWS, Google Cloud, Microsoft Azure).
* **Grassroots self-management**: Direct, horizontal control over server infrastructure without corporate gatekeepers or commercial middlemen.
* **Digital commons**: 100% free software (GPLv2+), open standards, decentralized architecture, zero external CDNs, and zero tracking or telemetry.

---

## Quickstart (1 Command)

Installation does not rely on outdated distro packages; it deploys via an automated shell script or native Docker Compose:

```bash
# 1. Clone repository
git clone git@github.com:AnARCHIS12/AlternC-modern.git
cd AlternC-modern

# 2. Run automated installer with port conflict detection
chmod +x install.sh
./install.sh
```

For non-interactive deployment (e.g., CI/CD automation):

```bash
./install.sh -y
```

### Direct Deployment via Docker Compose

```bash
# Copy template environment file
cp .env.example .env

# Start containers in background
docker compose up -d
```

The control panel will be available at `http://localhost:8080` (or your configured port).

---

## Architecture & Port Isolation

To guarantee seamless coexistence with other running services on the host machine, every exposed port is isolated and customizable in `.env`:

| Service | Default Host Port | Container Port | Environment Variable |
| :--- | :--- | :--- | :--- |
| **Web (HTTP)** | `8080` | `80` | `ALTERNC_HTTP_PORT` |
| **Web (HTTPS/SSL)** | `8443` | `443` | `ALTERNC_HTTPS_PORT` |
| **MariaDB** | `3307` | `3306` | `ALTERNC_MYSQL_PORT` |

---

## Modern 2026 Interface

* **Refined, responsive dashboard**: Sticky sidebar navigation with local SVG icons and top status bar.
* **Native dark and light modes**: Instant theme toggle stored in `localStorage` without flickering.
* **Spotlight palette (Ctrl+K)**: Keyboard command bar for quickly finding domains, mailboxes, and administrative tools.
* **Zero external dependencies**: System fonts, local vectors, and offline-first execution.

---

## Project Structure

```text
.
├── Dockerfile             # Container definition running PHP 8.3 Apache
├── docker-compose.yml     # Orchestration for Web and MariaDB 10.11
├── install.sh             # Modern installer with automatic port checking
├── .env.example           # Configuration template for ports and secrets
├── bureau/                # Web control panel in PHP
│   ├── admin/             # Updated administrative views and controllers
│   └── class/             # Core classes and database abstraction
├── docs/                  # Offline-first documentation portal (0% CDN)
│   └── index.html         # Complete guide with local search and theme toggle
└── README.md              # Main entry point documentation in Esperanto
```

---

## Contribution & License

Contributions are welcome in alignment with free software principles, inclusive language, and digital emancipation.

* **License**: GNU General Public License v2 or later (GPL-2.0-or-later). See [COPYING](COPYING).

<p align="center">
  <img src="bureau/admin/images/logo.png" alt="AlternC" width="300" />
</p>

# AlternC

> Plataforma libre, emancipadora y autogestionada para alojamiento web y correo electrónico, completamente modernizada con Docker, PHP 8.3 y MariaDB.

<div align="center">

**Lingvoj / Languages:** [Esperanto](README.md) • [Français](README.fr.md) • [English](README.en.md) • [Español](README.es.md)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Versi%C3%B3n-3.5%20Modern-2563eb?style=flat-square" alt="Versión" />
  <img src="https://img.shields.io/badge/PHP-8.3%20Activo-10b981?style=flat-square" alt="PHP 8.3" />
  <img src="https://img.shields.io/badge/Contenedor-Docker%20Compose-059669?style=flat-square" alt="Docker Compose" />
  <img src="https://img.shields.io/badge/MariaDB-10.11%20LTS-0284c7?style=flat-square" alt="MariaDB 10.11" />
  <img src="https://img.shields.io/badge/CDN-0%25%20(Aut%C3%B3nomo)-0d9488?style=flat-square" alt="Sin-CDN" />
  <img src="https://img.shields.io/badge/%C3%89tica-Autogesti%C3%B3n%20Anticapitalista-7c3aed?style=flat-square" alt="Autogestión" />
  <img src="https://img.shields.io/badge/Emoji-0%25%20(Pro)-6366f1?style=flat-square" alt="Sin-Emoji" />
  <img src="https://img.shields.io/badge/Licencia-GPL--2.0%2B-64748b?style=flat-square" alt="GPLv2+" />
</p>

---

## Descripción

**AlternC** es una plataforma histórica de software libre concebida para brindar a colectivos, asociaciones y personas el control absoluto y autogestionado sobre sus servicios de internet (servidores web, cuentas de correo, FTP, bases de datos y DNS).

Modernizada para satisfacer los estándares operativos actuales, AlternC descarta los empaquetados obsoletos y adopta un despliegue aislado y seguro mediante **Docker y Docker Compose**, funcionando sobre **PHP 8.3** y **MariaDB 10.11 LTS**.

### Ética Anticapitalista y Bienes Comunes

* **Rechazo a las Big Tech y cercamientos comerciales**: Resistencia activa frente al capitalismo de vigilancia y los monopolios de nubes privativas (AWS, Google Cloud, Microsoft Azure).
* **Autogestión comunitaria**: Control horizontal y directo de los servidores e infraestructuras, sin tutelas corporativas ni intermediarios mercantiles.
* **Bienes comunes digitales**: Software 100% libre (GPLv2+), protocolos abiertos, cero CDN externas y cero rastreo o telemetría.

---

## Inicio Rápido (1 Comando)

La instalación no requiere antiguos paquetes del sistema; se ejecuta de forma automatizada mediante un script en línea de comandos o mediante Docker Compose:

```bash
# 1. Clonar el repositorio
git clone git@github.com:AnARCHIS12/AlternC-modern.git
cd AlternC-modern

# 2. Iniciar la instalación con detección de puertos libres
chmod +x install.sh
./install.sh
```

Para una instalación automatizada sin intervención (ej. CI/CD):

```bash
./install.sh -y
```

### Despliegue directo con Docker Compose

```bash
# Copiar plantilla de variables de entorno
cp .env.example .env

# Iniciar los contenedores en segundo plano
docker compose up -d
```

El panel de administración estará disponible en `http://localhost:8080` (o el puerto configurado).

---

## Arquitectura y Aislamiento de Puertos

Para asegurar la coexistencia armónica con otros servicios en la máquina anfitriona, cada puerto expuesto está aislado y configurable en `.env`:

| Servicio | Puerto Anfitrión por Defecto | Puerto Contenedor | Variable de Entorno |
| :--- | :--- | :--- | :--- |
| **Web (HTTP)** | `8080` | `80` | `ALTERNC_HTTP_PORT` |
| **Web (HTTPS/SSL)** | `8443` | `443` | `ALTERNC_HTTPS_PORT` |
| **MariaDB** | `3307` | `3306` | `ALTERNC_MYSQL_PORT` |

---

## Interfaz Contemporánea 2026

* **Diseño limpio y adaptable**: Barra lateral con iconos SVG locales y barra superior con estado del servidor.
* **Modos claro y oscuro nativos**: Cambio instantáneo almacenado en `localStorage` sin parpadeos.
* **Búsqueda Spotlight (Ctrl+K)**: Paleta de comandos rápida para localizar dominios y utilidades con el teclado.
* **Cero dependencias externas**: Tipografía de sistema, vectores locales y funcionamiento 100% autónomo (offline-first).

---

## Estructura del Proyecto

```text
.
├── Dockerfile             # Definición del contenedor bajo PHP 8.3 Apache
├── docker-compose.yml     # Orquestación de Web y MariaDB 10.11
├── install.sh             # Script de instalación moderno con verificación de puertos
├── .env.example           # Plantilla de configuración de puertos y credenciales
├── bureau/                # Panel de control web en PHP
│   ├── admin/             # Vistas y controladores actualizados
│   └── class/             # Clases del núcleo y abstracción de datos
├── docs/                  # Portal de documentación autónomo (0% CDN)
│   └── index.html         # Guía completa con búsqueda local y cambio de tema
└── README.md              # Documentación principal en esperanto
```

---

## Contribución y Licencia

Las contribuciones comunitarias son bienvenidas bajo los principios del software libre, el lenguaje inclusivo y la defensa de los bienes comunes digitales.

* **Licencia**: Licencia Pública General de GNU v2 o posterior (GPL-2.0-or-later). Ver [COPYING](COPYING).

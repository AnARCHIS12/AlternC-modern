# AlternC

> Emancipa, memmastrumata kaj kontraŭkapitalisma libera platformo por gastigado de retpaĝoj kaj retpoŝtoj, plene modernigita per Docker, PHP 8.3 kaj MariaDB.

<div align="center">

**Lingvoj / Languages:** [Esperanto](README.md) • [Français](README.fr.md) • [English](README.en.md) • [Español](README.es.md)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Versio-3.5%20Modern-2563eb?style=flat-square" alt="Versio" />
  <img src="https://img.shields.io/badge/PHP-8.3%20Aktiva-10b981?style=flat-square" alt="PHP 8.3" />
  <img src="https://img.shields.io/badge/Ujo-Docker%20Compose-059669?style=flat-square" alt="Docker Compose" />
  <img src="https://img.shields.io/badge/MariaDB-10.11%20LTS-0284c7?style=flat-square" alt="MariaDB 10.11" />
  <img src="https://img.shields.io/badge/CDN-0%25%20(Aŭtonoma)-0d9488?style=flat-square" alt="Sen-CDN" />
  <img src="https://img.shields.io/badge/Etiko-Kontraŭkapitalisma%20Memmastrumado-7c3aed?style=flat-square" alt="Liberecana" />
  <img src="https://img.shields.io/badge/Emoji-0%25%20(Profesia)-6366f1?style=flat-square" alt="Sen-Emoji" />
  <img src="https://img.shields.io/badge/Permesilo-GPL--2.0%2B-64748b?style=flat-square" alt="GPLv2+" />
</p>

---

## Priskribo

**AlternC** estas historia kaj memstara libera programara aro celanta doni al kolektivoj, asocioj kaj individuoj la plenan kontrolon super siaj retservoj (TTT, retpoŝto, dosiertransigo, datumbazoj, DNS).

Moderne adaptita por la nuntempaj bezonoj, AlternC liberiĝas de malnovaj instal-metodoj por proponi puran, sekuran kaj izulitan deplojon per **Docker kaj Docker Compose**, funkcianta sur **PHP 8.3** kaj **MariaDB 10.11 LTS**.

### Etiko kaj Ciferecaj Komunaĵoj

* **Rifuzo de Big Tech kaj komerca kapitalismo**: Batalo kontraŭ la monopoloj de privataj nuboj (AWS, Google Cloud, Microsoft Azure) kaj gvata kapitalismo.
* **Kolektiva memmastrumado**: Rekta povo super la serviloj, sen komercaj perantoj kaj sen fremda kuratoreco.
* **Ciferecaj komunaĵoj**: 100% libera programaro (GPLv2+), malfermitaj normoj, nula ekstera CDN, nula sekvado aŭ telemetrio.

---

## Rapida Ekfunkciigo (1 Komando)

La instalado ne plu dependas de malnovaj debian-pakoj; ĝi plenumiĝas rekte per aŭtomata komandlinia skripto aŭ per Docker Compose.

```bash
# 1. Kloni la deponejon
git clone git@github.com:AnARCHIS12/AlternC-modern.git
cd AlternC-modern

# 2. Lanĉi la aŭtomatan instaladon kun serĉo de liberaj pordoj
chmod +x install.sh
./install.sh
```

Por seninteraga instalado (ekzemple en CI/CD):

```bash
./install.sh -y
```

### Rekta deplojo per Docker Compose

```bash
# Kopii la agordan modelon
cp .env.example .env

# Lanĉi la servojn en fono
docker compose up -d
```

La administrejo estos alirebla ĉe `http://localhost:8080` (aŭ la elektita pordo).

---

## Arkitekturo kaj Pordo-Izolado

Por certigi kunekzistadon kun ekzistantaj servoj sur la gastiganta maŝino, la pordoj estas defaŭlte izolitaj kaj agordeblaj en `.env`:

| Servo | Defaŭlta Gastiga Pordo | Uja Pordo | Medivariablo |
| :--- | :--- | :--- | :--- |
| **TTT (HTTP)** | `8080` | `80` | `ALTERNC_HTTP_PORT` |
| **TTT (HTTPS/SSL)** | `8443` | `443` | `ALTERNC_HTTPS_PORT` |
| **MariaDB** | `3307` | `3306` | `ALTERNC_MYSQL_PORT` |

---

## Moderna Panelo 2026

* **Svelta kaj adapta fasado**: Flanka navigado kun vektoraj SVG-simboloj, supra stirbreto kun servilaj indikiloj.
* **Malhela kaj hela etosoj**: Tuja ŝanĝo per `localStorage` sen ekrana flagrado.
* **Komand-paletro (Stirklavo+K)**: Rapida serĉado de domajnoj, retpoŝtoj kaj iloj rekte per la klavaro.
* **0% Eksteraj Dependecoj**: Ĉiuj tiparoj, skriptoj kaj vektoroj estas lokaj (offline-first).

---

## Dosieruja Strukturo

```text
.
├── Dockerfile             # Konstruo de la ujo sub PHP 8.3 Apache
├── docker-compose.yml     # Orkestrado de la TTT-servo kaj MariaDB 10.11
├── install.sh             # Aŭtomata instal-skripto sen pordo-konfliktoj
├── .env.example           # Ŝablono por pordoj kaj pasvortoj
├── bureau/                # Reta administrejo (PHP)
│   ├── admin/             # Fasado kaj modernaj PHP-paĝoj
│   └── class/             # Kernaj klasoj kaj modelo
├── docs/                  # Loka dokumentara portalo (sen CDN)
│   └── index.html         # Plena teknika gvidilo kun serĉilo kaj etoso
└── README.md              # Ĉefa dokumentaro en Esperanto
```

---

## Kontribuado kaj Permesilo

Kolektivaj kontribuoj estas bonvenaj sub la principoj de libera kodo, inkluziva lingvaĵo kaj respekto al ciferecaj komunaĵoj.

* **Permesilo**: GNU General Public License v2 aŭ posta (GPL-2.0-or-later). Vidu [COPYING](COPYING).

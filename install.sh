#!/usr/bin/env bash
# ==============================================================================
# AlternC Cloud Platform - Professional CLI Installer
# Autonomous port allocation, container orchestration & environment setup
# ==============================================================================

set -eo pipefail

# ANSI Color Palette (Minimalist & Professional)
CLR_RESET="\033[0m"
CLR_BOLD="\033[1m"
CLR_DIM="\033[2m"
CLR_ITALIC="\033[3m"

CLR_GRAY="\033[38;5;244m"
CLR_LIGHT_GRAY="\033[38;5;250m"
CLR_WHITE="\033[38;5;255m"

CLR_CYAN="\033[38;5;74m"
CLR_BLUE="\033[38;5;68m"
CLR_PURPLE="\033[38;5;141m"
CLR_GREEN="\033[38;5;78m"
CLR_YELLOW="\033[38;5;215m"
CLR_RED="\033[38;5;203m"

# Glyphs
GL_CHECK="${CLR_GREEN}✓${CLR_RESET}"
GL_CROSS="${CLR_RED}✕${CLR_RESET}"
GL_ARROW="${CLR_CYAN}›${CLR_RESET}"
GL_BULLET="${CLR_GRAY}•${CLR_RESET}"
GL_DOT_ACTIVE="${CLR_CYAN}●${CLR_RESET}"
GL_DOT_INACTIVE="${CLR_GRAY}○${CLR_RESET}"

print_banner() {
  clear 2>/dev/null || true
  echo ""
  echo -e "  ${CLR_BOLD}${CLR_WHITE}AlternC${CLR_RESET} ${CLR_CYAN}v3.5${CLR_RESET} ${CLR_DIM}— Cloud Platform Docker Setup${CLR_RESET}"
  echo -e "  ${CLR_GRAY}─────────────────────────────────────────────────────────────────${CLR_RESET}"
  echo ""
}

# Spinner function without tacky symbols
run_task() {
  local label="$1"
  shift
  local pid
  local spinchars=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
  local i=0

  echo -ne "  ${CLR_CYAN}›${CLR_RESET} ${label}..."
  "$@" > /dev/null 2>&1 &
  pid=$!

  while kill -0 "$pid" 2>/dev/null; do
    i=$(( (i+1) % 10 ))
    echo -ne "\r  ${CLR_CYAN}${spinchars[$i]}${CLR_RESET} ${label}..."
    sleep 0.08
  done

  if wait "$pid"; then
    echo -e "\r  ${GL_CHECK} ${label}"
    return 0
  else
    echo -e "\r  ${GL_CROSS} ${label} ${CLR_RED}(failed)${CLR_RESET}"
    return 1
  fi
}

# Check if a port is open/free on localhost
is_port_free() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ! ss -tlpn | grep -q ":${port} "
  elif command -v netstat >/dev/null 2>&1; then
    ! netstat -tlpn 2>/dev/null | grep -q ":${port} "
  elif command -v lsof >/dev/null 2>&1; then
    ! lsof -i ":${port}" >/dev/null 2>&1
  else
    (echo > "/dev/tcp/127.0.0.1/${port}") 2>/dev/null && return 1 || return 0
  fi
}

find_next_free_port() {
  local port="$1"
  while ! is_port_free "$port"; do
    port=$((port + 1))
  done
  echo "$port"
}

generate_secret() {
  head /dev/urandom | tr -dc A-Za-z0-9 | head -c "${1:-16}"
}

print_banner

# Step 1: Pre-flight checks
echo -e "  ${CLR_BOLD}[1/4] Environment verification${CLR_RESET}"

if ! command -v docker >/dev/null 2>&1; then
  echo -e "  ${GL_CROSS} Docker runtime not found. Please install Docker Engine."
  exit 1
fi
DOCKER_VER=$(docker --version | awk '{print $3}' | tr -d ',')
echo -e "  ${GL_CHECK} Docker Engine detected ${CLR_DIM}(${DOCKER_VER})${CLR_RESET}"

COMPOSE_CMD=""
if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD="docker-compose"
else
  echo -e "  ${GL_CROSS} Docker Compose plugin not found."
  exit 1
fi
COMPOSE_VER=$($COMPOSE_CMD version | awk '{print $4}' | tr -d 'v,')
echo -e "  ${GL_CHECK} Docker Compose detected ${CLR_DIM}(${COMPOSE_VER})${CLR_RESET}"

if ! docker info >/dev/null 2>&1; then
  echo -e "  ${GL_CROSS} Docker daemon is not running."
  exit 1
fi
echo -e "  ${GL_CHECK} Daemon socket active"
echo ""

# Step 2: Port allocation and conflict detection
echo -e "  ${CLR_BOLD}[2/4] Network & Port configuration${CLR_RESET}"

AUTO_CONFIRM=false
for arg in "$@"; do
  if [ "$arg" == "-y" ] || [ "$arg" == "--yes" ]; then
    AUTO_CONFIRM=true
  fi
done

HTTP_SUGGESTION=$(find_next_free_port 8080)
HTTPS_SUGGESTION=$(find_next_free_port 8443)
MYSQL_SUGGESTION=$(find_next_free_port 3307)

echo -e "  ${CLR_DIM}Scanning local host ports...${CLR_RESET}"
if is_port_free 8080; then
  echo -e "  ${GL_CHECK} Port 8080 (HTTP) is available"
else
  echo -e "  ${CLR_YELLOW}!${CLR_RESET} Port 8080 is already in use. Suggested: ${CLR_CYAN}${HTTP_SUGGESTION}${CLR_RESET}"
fi

if is_port_free 8443; then
  echo -e "  ${GL_CHECK} Port 8443 (HTTPS) is available"
else
  echo -e "  ${CLR_YELLOW}!${CLR_RESET} Port 8443 is already in use. Suggested: ${CLR_CYAN}${HTTPS_SUGGESTION}${CLR_RESET}"
fi

if is_port_free 3307; then
  echo -e "  ${GL_CHECK} Port 3307 (Database) is available"
else
  echo -e "  ${CLR_YELLOW}!${CLR_RESET} Port 3307 is already in use. Suggested: ${CLR_CYAN}${MYSQL_SUGGESTION}${CLR_RESET}"
fi

if [ "$AUTO_CONFIRM" = false ]; then
  echo ""
  read -r -p "  ? Web HTTP port [${HTTP_SUGGESTION}]: " INPUT_HTTP
  TARGET_HTTP_PORT="${INPUT_HTTP:-$HTTP_SUGGESTION}"

  read -r -p "  ? Web HTTPS port [${HTTPS_SUGGESTION}]: " INPUT_HTTPS
  TARGET_HTTPS_PORT="${INPUT_HTTPS:-$HTTPS_SUGGESTION}"

  read -r -p "  ? MySQL host port [${MYSQL_SUGGESTION}]: " INPUT_MYSQL
  TARGET_MYSQL_PORT="${INPUT_MYSQL:-$MYSQL_SUGGESTION}"

  read -r -p "  ? Fully Qualified Domain / Host [localhost]: " INPUT_FQDN
  TARGET_FQDN="${INPUT_FQDN:-localhost}"

  DEFAULT_PASS=$(generate_secret 12)
  read -r -p "  ? Admin password [${DEFAULT_PASS}]: " INPUT_PASS
  TARGET_ADMIN_PASS="${INPUT_PASS:-$DEFAULT_PASS}"
else
  TARGET_HTTP_PORT="$HTTP_SUGGESTION"
  TARGET_HTTPS_PORT="$HTTPS_SUGGESTION"
  TARGET_MYSQL_PORT="$MYSQL_SUGGESTION"
  TARGET_FQDN="localhost"
  TARGET_ADMIN_PASS=$(generate_secret 12)
fi

DB_SECRET=$(generate_secret 24)
DB_ROOT_SECRET=$(generate_secret 24)

# Generate .env
cat <<EOF > .env
# AlternC Production Environment Configuration
ALTERNC_HTTP_PORT=${TARGET_HTTP_PORT}
ALTERNC_HTTPS_PORT=${TARGET_HTTPS_PORT}
ALTERNC_MYSQL_PORT=${TARGET_MYSQL_PORT}
ALTERNC_BIND_IP=0.0.0.0
ALTERNC_DB_BIND_IP=127.0.0.1
ALTERNC_FQDN=${TARGET_FQDN}
ALTERNC_ADMIN_USER=admin
ALTERNC_ADMIN_PASS=${TARGET_ADMIN_PASS}
DB_NAME=alternc
DB_USER=alternc
DB_PASS=${DB_SECRET}
DB_ROOT_PASS=${DB_ROOT_SECRET}
EOF

echo ""
echo -e "  ${GL_CHECK} Environment file created ${CLR_DIM}(.env)${CLR_RESET}"
echo ""

# Step 3: Container Orchestration
echo -e "  ${CLR_BOLD}[3/4] Container orchestration${CLR_RESET}"
echo -e "  ${CLR_DIM}Building container images and starting services...${CLR_RESET}"
$COMPOSE_CMD up -d --build

echo ""
# Step 4: Health check
echo -e "  ${CLR_BOLD}[4/4] Service health validation${CLR_RESET}"

PANEL_READY=false
for i in {1..40}; do
  if curl -s "http://127.0.0.1:${TARGET_HTTP_PORT}/" >/dev/null 2>&1; then
    PANEL_READY=true
    break
  fi
  sleep 2
  echo -ne "\r  ${CLR_CYAN}›${CLR_RESET} Awaiting HTTP response from container (${i}/40s)..."
done
echo ""

if [ "$PANEL_READY" = true ]; then
  echo -e "  ${GL_CHECK} Control panel successfully responding on port ${CLR_CYAN}${TARGET_HTTP_PORT}${CLR_RESET}"
else
  echo -e "  ${CLR_YELLOW}!${CLR_RESET} Services launched in background. Check container logs with:"
  echo -e "    ${CLR_GRAY}${COMPOSE_CMD} logs -f${CLR_RESET}"
fi

# Summary Card
echo ""
echo -e "  ${CLR_GRAY}┌──────────────────────────────────────────────────────────────┐${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${CLR_BOLD}${CLR_WHITE}AlternC Deployment Summary${CLR_RESET}                                   ${CLR_GRAY}│${CLR_RESET}"
echo -e "  ${CLR_GRAY}├──────────────────────────────────────────────────────────────┤${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${CLR_BOLD}Dashboard URL${CLR_RESET}   ${CLR_CYAN}http://${TARGET_FQDN}:${TARGET_HTTP_PORT}/${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${CLR_BOLD}Username${CLR_RESET}        ${CLR_WHITE}admin${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${CLR_BOLD}Password${CLR_RESET}        ${CLR_YELLOW}${TARGET_ADMIN_PASS}${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${CLR_BOLD}Port Mappings${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${GL_BULLET} Web HTTP      ${CLR_CYAN}${TARGET_HTTP_PORT}${CLR_RESET} ${CLR_GRAY}→${CLR_RESET} 80"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${GL_BULLET} Web HTTPS     ${CLR_CYAN}${TARGET_HTTPS_PORT}${CLR_RESET} ${CLR_GRAY}→${CLR_RESET} 443"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${GL_BULLET} Database      ${CLR_CYAN}${TARGET_MYSQL_PORT}${CLR_RESET} ${CLR_GRAY}→${CLR_RESET} 3306"
echo -e "  ${CLR_GRAY}│${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${CLR_BOLD}Management Commands${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${GL_BULLET} View logs     ${CLR_GRAY}${COMPOSE_CMD} logs -f${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${GL_BULLET} Stop panel    ${CLR_GRAY}${COMPOSE_CMD} stop${CLR_RESET}"
echo -e "  ${CLR_GRAY}│${CLR_RESET}  ${GL_BULLET} Restart       ${CLR_GRAY}${COMPOSE_CMD} restart${CLR_RESET}"
echo -e "  ${CLR_GRAY}└──────────────────────────────────────────────────────────────┘${CLR_RESET}"
echo ""

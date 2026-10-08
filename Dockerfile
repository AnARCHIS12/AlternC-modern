FROM php:8.3-apache

LABEL maintainer="AlternC Modern Docker <alternc.org>"
LABEL description="AlternC Modern Cloud Control Panel in Docker"

# Install system dependencies & Debian javascript packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    mariadb-client \
    gettext \
    locales \
    libjs-jquery \
    libjs-jquery-ui \
    libjs-jquery-tablesorter \
    javascript-common \
    libcurl4-openssl-dev \
    libxml2-dev \
    libzip-dev \
    libicu-dev \
    zip \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Setup UTF-8 locales
RUN sed -i -e 's/# fr_FR.UTF-8 UTF-8/fr_FR.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# nl_NL.UTF-8 UTF-8/nl_NL.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

ENV LANG=fr_FR.UTF-8
ENV LANGUAGE=fr_FR:en
ENV LC_ALL=fr_FR.UTF-8

# Install modern PHP 8.3 extensions
RUN docker-php-ext-configure intl && \
    docker-php-ext-install -j$(nproc) \
    pdo_mysql \
    mysqli \
    curl \
    xml \
    zip \
    gettext \
    intl \
    opcache

# Recommended PHP production settings
RUN { \
    echo 'opcache.memory_consumption=128'; \
    echo 'opcache.interned_strings_buffer=8'; \
    echo 'opcache.max_accelerated_files=4000'; \
    echo 'opcache.revalidate_freq=2'; \
    echo 'opcache.enable_cli=1'; \
    echo 'upload_max_filesize=64M'; \
    echo 'post_max_size=64M'; \
    echo 'memory_limit=256M'; \
    echo 'display_errors=Off'; \
    echo 'display_startup_errors=Off'; \
    echo 'log_errors=On'; \
    echo 'error_reporting=E_ALL & ~E_DEPRECATED & ~E_STRICT & ~E_NOTICE'; \
} > /usr/local/etc/php/conf.d/alternc-recommended.ini

# Enable Apache modules
RUN a2enmod rewrite headers alias

# Create AlternC system folders
RUN mkdir -p /usr/share/alternc/panel \
    /usr/lib/alternc \
    /usr/share/alternc/install \
    /etc/alternc/templates/apache2 \
    /var/lib/alternc/panel \
    /var/lib/alternc/apache-vhost/manual \
    /var/log/alternc \
    /var/alternc/html \
    /var/alternc/mail \
    /run/alternc

# Copy codebase
COPY bureau/ /usr/share/alternc/panel/
COPY src/ /usr/lib/alternc/
COPY install/ /usr/share/alternc/install/
COPY etc/alternc/ /etc/alternc/

# Set version
RUN sed -i -e "s/@@REPLACED_DURING_BUILD@@/3.5-docker/" \
    /usr/share/alternc/panel/class/local.php \
    /usr/share/alternc/install/alternc.install

# Compile gettext catalogs
RUN find /usr/share/alternc/panel/locales -maxdepth 1 -mindepth 1 -type d -name "*_*" | while read d; do \
      if [ -d "$d/LC_MESSAGES" ]; then \
        cd "$d/LC_MESSAGES" && \
        if [ -f alternc ] && [ ! -f alternc_base.po ]; then cp alternc alternc_base.po; fi && \
        if ls *.po 1> /dev/null 2>&1; then \
          msgcat --use-first *.po alternc 2>/dev/null > alternc.po || cat *.po > alternc.po; \
          msgfmt alternc.po -o alternc.mo 2>/dev/null || true; \
        fi; \
      fi; \
    done

# Apache site config
COPY docker/apache-alternc.conf /etc/apache2/sites-available/000-default.conf

# Entrypoint
COPY docker/entrypoint.sh /usr/local/bin/alternc-entrypoint.sh
RUN chmod +x /usr/local/bin/alternc-entrypoint.sh

WORKDIR /usr/share/alternc/panel

EXPOSE 80 443

ENTRYPOINT ["/usr/local/bin/alternc-entrypoint.sh"]
CMD ["apache2-foreground"]

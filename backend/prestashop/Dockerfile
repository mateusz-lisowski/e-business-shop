FROM prestashop/prestashop:1.7.8

# Ustawienia katalogów
WORKDIR /var/www/html

# Usunięcie zawartości katalogu /var/www/html (jeśli jest to konieczne)
RUN rm -rf /var/www/html/*

# Skopiowanie lokalnych plików PrestaShop
COPY ./prestashop_files/ /var/www/html/

# Usunięcie folderu `install` (jeśli występuje w obrazie bazowym)
RUN rm -rf /var/www/html/install

# Skopiowanie konfiguracji bazy danych
COPY ./db_backup.sql /docker-entrypoint-initdb.d/db_backup.sql

# Ustawienia uprawnień
RUN chmod -R 777 /var/www/html/var/cache /var/www/html/var/logs

# Skopiowanie środowisk (pliki .env do modułów)
COPY ./checkout.env /var/www/html/modules/ps_checkout/.env
COPY ./mbo.env /var/www/html/modules/ps_mbo/.env
COPY ./metrics.env /var/www/html/modules/ps_metrics/.env

# Włącz moduły Apache potrzebne do SSL i przepisywania URL
RUN a2enmod ssl rewrite

# Skopiowanie pliku konfiguracji SSL dla Apache
COPY ./apache-ssl.conf /etc/apache2/sites-available/default-ssl.conf

# Aktywacja konfiguracji SSL
RUN a2ensite default-ssl

# Skonfigurowanie serwera Apache
CMD ["apache2-foreground"]

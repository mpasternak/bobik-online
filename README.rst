bobik-ai
========

Czat-bot preanestetyczny.

.. include:: <isonum.txt>

|copy| 2024 Michał Pasternak

Licencja MIT.

Najprościej uruchomisz:

1. Ściągnij sobie Dockera `stąd <https://www.docker.com/products/docker-desktop/>`_

2. Ściągnij to repozytorium kodu na dysk lokalny:

.. code-block:: shell

    $ git clone https://github.com/mpasternak/bobik-online.git

3. Wejdź do katalogu repozytorium:

.. code-block:: shell

    $ cd bobik-online

4. Uruchom serwis:

.. code-block:: shell

    $ docker compose up

5. Normalne jest, że krok 4 trochę potrwa, będzie też wyświetlać duże ilości tekstu. Gdy
   serwis uruchomi się, będzie dostępny z poziomu przeglądarki internetowej pod adresem: http://127.0.0.1:8000/

6. System wymaga wpisania klucza do API Anthropic oraz zasilenia swojego konta funduszami, który możesz
   nabyć `tutaj <https://console.anthropic.com/settings/plans>`_ .

7. Konto administratora to "admin"; początkowe hasło ustawisz po uruchomieniu systemu.

8. Konfiguracja wysyłki e-mail wymaga edycji pliku docker-compose.yml lub .env.docker .
# SIWA Benutzerverwaltung (FastAPI Projekt)

Dies ist ein FastAPI-Projekt, das eine einfache Benutzerverwaltung mit einer MariaDB-Datenbank implementiert. Das
Projekt ermöglicht das Anzeigen und Hinzufügen von Benutzern über ein Webinterface mit AJAX-Unterstützung.

## Funktionen

* Anzeigen aller Benutzer aus der Datenbank.
* Hinzufügen neuer Benutzer über ein Formular.
* AJAX-basierte Formularübermittlung (kein Neuladen der Seite).
* Validierung von Formulareingaben.
* **Optional:** Light/Dark Mode-Umschaltung mit Speicherung in der Sitzung (Cookie).
* **(Vorhanden):** Beinhaltet ein voll funktionsfähiges OAuth2-Authentifizierungssystem mit **JWT-Token** (siehe
  Endpunkte unter `/auth`, `/posts`, `/votes`).

## Verwendete Technologien

* **Backend:** FastAPI
* **Datenbank:** MariaDB (via `mysql-connector-python`)
* **ORM:** SQLAlchemy
* **Frontend:** Jinja2 (für Templating), HTML5, CSS3, JavaScript (fetch API)
* **Validierung:** Pydantic
* **Authentifizierung:** OAuth2 mit JWT-Token (`python-jose`, `bcrypt`)

## 1. Setup & Installation

**Voraussetzungen:**

* Python 3.8+
* Eine laufende MariaDB Instanz (oder MySQL)
* Docker (optional, falls du die Datenbank in einem Container betreiben möchtest)

**Schritte:**

1. **Repository klonen (oder ZIP entpacken):**
   ```bash
   git clone https://github.com/Esperon1/fast-api-project
   cd fast-api-project
   ```

2. **Virtuelle Umgebung erstellen & aktivieren:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # (Für Windows: venv\Scripts\activate)
   ```

3. **Abhängigkeiten installieren:**
   ```bash
   
   pip install "fastapi[all]" sqlalchemy mysql-connector-python pydantic-settings python-jose[cryptography] bcrypt jinja2
   ```

4. **Datenbank einrichten:**
    * Erstelle manuell eine Datenbank in MariaDB:
        ```sql
        CREATE DATABASE siwa_db_fastapi;
        ```
    * Oder run in einem Docker-Container:
      ```bash
      docker run --name siwa-db -e MARIADB_ROOT_PASSWORD=dein_passwort -p 3306:3306 -d mariadb:latest
      ```

5. **`.env` Datei konfigurieren:**
    * Erstelle eine Datei namens `.env` im Stammverzeichnis des Projekts.
    * Kopiere den Inhalt von `.env.example` (siehe unten) hinein und passe die Werte für deine Datenbank an.

   ***.env.example:***
   ```ini
   # MariaDB/MySQL Einstellungen
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=siwa_db_fastapi
   DB_USER=root
   DB_PASSWORD= ... (dein Passwort hier) ...

   # JWT Einstellungen (falls für API-Teile verwendet)
   DB_SECRET_KEY= ... (ein sicherer geheimer Schlüssel) ...
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

## 2. Projekt starten

Führe den folgenden Befehl im Stammverzeichnis des Projekts aus:

```bash

uvicorn app.main:app --reload
```

## 3. Anwendung aufrufen

Die Benutzerliste ist unter der folgenden URL im Browser verfügbar:
http://127.0.0.1:8000/


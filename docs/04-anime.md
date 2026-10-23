# 4. Anime mit Shoko + Shokofin

Jellyfins eigene Erkennung (TVDB/TMDB) passt bei Anime oft nicht: Staffeln sind anders
gezählt, OVAs/Specials landen falsch. **Shoko** erkennt jede Datei über ihren Hash bei AniDB,
**Shokofin** baut daraus in Jellyfin saubere Serien.

## Shoko (8111)

1. Weboberfläche → Erststart: AniDB-Konto eintragen (kostenlos registrieren).
2. Import-Ordner: `/anime` (Typ „Source“, „Watch“ an).
3. Shoko hasht und erkennt alle Dateien – beim ersten Mal dauert das (AniDB drosselt).

## Shokofin (Jellyfin-Plugin)

1. Jellyfin → Plugins → Repositories: Shokofin-Repo hinzufügen, Plugin installieren, neu starten.
2. Plugin-Einstellungen: Server `http://shoko:8111`, mit Shoko-Benutzer anmelden.
3. Anime-Bibliothek in Jellyfin: Typ Serien, Ordner `/anime`.
4. In Shokofin für diese Bibliothek das **VFS** (Virtual File System) aktivieren. Shokofin legt
   dann eine Ordnerstruktur aus Links an, die Jellyfin wie eine normale Serienbibliothek liest.

## Anime-Trailer (optional)

Trailarr findet Trailer für normale Serien. Bei Anime passt die Zuordnung nicht direkt, weil
Shokofin die Serien anders schneidet (eine Sonarr-Serie kann in mehrere Shoko-Serien zerfallen).
[`scripts/anime-trailer/`](../scripts/anime-trailer/) löst das:

1. In Trailarr zwei Profile „Anime Trailers“ und „Anime Teaser“ anlegen:
   - Filter: Serien, deren Ordner mit dem Anime-Ordner beginnt
   - Eigener Ordner: `/anime-trailer/{txdb_id}`
   - Suche z. B. `{title} anime trailer deutsch`
2. `anime_trailer_link.py` (Probelauf) schreibt einen Bericht, welche Trailer eindeutig zu
   welchem Shokofin-Eintrag gehören – ohne Namensvergleich, nur über die Links im VFS.
3. Bericht prüfen, falsche Videos in `sperrliste.txt`, Sonderfälle in `zuordnung.txt`.
4. `anime_trailer_link.py --apply` legt Links im VFS (`trailers/`) an und lässt Jellyfin die
   betroffenen Serien neu einlesen.
5. Für Serien, die nicht eindeutig sind: Videos von Hand in `manuell.txt` eintragen und mit
   `manuell_laden.sh` laden.

## Unerkannte Dateien mit Claude zuordnen (optional)

Shoko erkennt eine Datei nur, wenn AniDB ihren Hash kennt. Bei ganz neuen Folgen (Sonarr lädt
sie am Ausstrahlungstag) ist das oft noch nicht der Fall – die Datei bleibt „unerkannt“ und
fehlt in Jellyfin. Von Hand zuordnen ist mühsam, ein starres Skript nach Dateinamen zu ungenau:
Sonarr zählt nach TVDB, AniDB führt jede Staffel als eigene Serie mit eigener Zählung.

[`scripts/shoko-zuordnung/`](../scripts/shoko-zuordnung/) lässt diese Fälle von **Claude**
(Anthropic-API) entscheiden:

1. Ein systemd-Timer schaut alle 10 Minuten in Shoko nach unerkannten Dateien. Nur wenn es eine
   gibt, die älter als 30 Minuten ist (Shoko hatte Zeit, sie selbst zu erkennen), wird Claude gefragt.
2. Claude bekommt Pfad, Größe und Importdatum und darf in Shoko nur **lesen**: Serien suchen,
   Folgen und schon zugeordnete Dateien ansehen. Die Nachbardateien (S03E01–E03 → Folge 1–3)
   verraten die Zählung. Fehlt die passende Folge, weil die Shoko-Daten veraltet sind, darf
   Claude die Serie neu von AniDB laden lassen (höchstens alle 12 Stunden pro Serie).
3. Claude meldet Folge, Sicherheit und Begründung. **Zugeordnet wird nur bei Sicherheit „hoch“**,
   alles andere landet in `/var/lib/shoko-zuordnung/offen.json` und wird nach 6 Stunden erneut
   geprüft. Eine falsche Zuordnung ist schlimmer als keine.
4. Nach einer Zuordnung lässt das Skript die betroffene Serie in Jellyfin neu einlesen
   (Shokofin bekommt Zuordnungen über SignalR nicht immer mit). Ist die Serie in Jellyfin noch
   unbekannt, wird die Shokofin-Bibliothek eingelesen.

Von der neuen Datei bis Jellyfin dauert es so etwa 30–45 Minuten. Kosten: ein paar Cent pro
unerkannter Datei (Modell `claude-opus-5-5`).

### Einrichten

```bash
apt install python3-venv
mkdir -p /opt/media-stack/shoko-zuordnung && cp scripts/shoko-zuordnung/zuordnen.py /opt/media-stack/shoko-zuordnung/
cd /opt/media-stack/shoko-zuordnung && python3 -m venv venv && venv/bin/pip install anthropic

# Schlüssel (nur für root lesbar)
install -d -m 700 /root/.config/shoko-zuordnung && cd /root/.config/shoko-zuordnung
umask 077
nano shoko-key       # Shoko-API-Schlüssel, z. B. der aus der Shokofin-Konfiguration
nano jellyfin-key    # Jellyfin-API-Schlüssel (Dashboard → API-Schlüssel), optional
nano anthropic-key   # Schlüssel von console.anthropic.com

cp scripts/shoko-zuordnung/shoko-zuordnung.{service,timer} /etc/systemd/system/
systemctl daemon-reload && systemctl enable --now shoko-zuordnung.timer
```

Läuft das Skript nicht direkt auf dem Docker-Host, die Adressen über `SHOKO_URL` und
`JELLYFIN_URL` setzen (Standard `http://localhost:8111` bzw. `http://localhost:8096`).

### Erst probieren, dann scharf schalten

Solange es `/root/.config/shoko-zuordnung/scharf` nicht gibt, **schlägt das Skript nur vor**.
Ergebnisse stehen im Journal und in `offen.json`:

```bash
journalctl -u shoko-zuordnung.service -n 50
cat /var/lib/shoko-zuordnung/offen.json
```

Passen die Vorschläge, mit `touch /root/.config/shoko-zuordnung/scharf` freischalten. Das
Skript ordnet nur zu und liest Serien neu ein – es löscht, verschiebt oder ändert sonst nichts.

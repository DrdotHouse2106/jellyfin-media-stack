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

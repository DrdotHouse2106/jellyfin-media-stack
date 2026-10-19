# 7. Musik, Hörbücher, Bücher, YouTube

| Dienst | Port | Ordner | Apps |
|---|---|---|---|
| **Navidrome** | 4533 | `MUSIC_DIR` (nur lesend) | Subsonic-Apps (z. B. Symfonium, Substreamer, Amperfy) |
| **Audiobookshelf** | 8000 | `AUDIOBOOKS_DIR` | eigene App (Android/iOS), merkt Position |
| **Kavita** | 5000 | `BOOKS_DIR`, `MANGA_DIR` | Browser, OPDS-Reader |
| **Suwayomi** | 8081 | lädt nach `MANGA_DIR` | Weboberfläche |
| **Pinchflat** | 8945 | `YOUTUBE_DIR` | Ergebnis in Jellyfin/Audiobookshelf einbinden |

## Hinweise

- **Navidrome**: Last.fm-API-Key (optional) liefert Künstlerbilder und Biografien.
- **Lidarr + Navidrome**: Lidarr lädt nach `/music`, Navidrome liest denselben Ordner.
- **Suwayomi**: Erweiterungen (Quellen) in der Oberfläche installieren, Mangas zur Bibliothek
  hinzufügen, Downloads landen als CBZ in `MANGA_DIR` – Kavita liest sie automatisch.
- **Pinchflat**: Kanal/Playlist + Medienprofil anlegen. Für Jellyfin eine eigene Bibliothek
  „YouTube“ (Typ Heimvideos) auf `YOUTUBE_DIR`; für Podcasts lieber nur Audio und in
  Audiobookshelf einbinden.

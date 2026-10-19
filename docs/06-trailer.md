# 6. Trailer mit Trailarr

Trailarr (7889) liest die Bibliotheken von Radarr und Sonarr und legt passende YouTube-Trailer
als Datei neben Film/Serie (`<Film>/trailers/…`). Jellyfin zeigt sie als lokale Trailer –
ohne Werbung, ohne YouTube-Sperren, auch auf Geräten ohne YouTube.

1. Erster Login: `admin` / `trailarr` – **Passwort sofort ändern**.
2. Settings → Connections: Radarr und Sonarr (Host `radarr`/`sonarr`, API-Keys).
   Weil alle Container dieselben `/data`-Pfade nutzen, sind keine Pfad-Zuordnungen nötig.
3. Profile: Sprache/Suchbegriff anpassen, z. B. `{title} {year} trailer deutsch`.
4. Optional einen TMDB-API-Key hinterlegen – verbessert die Trefferauswahl.
5. Wartezeit zwischen Downloads nicht zu klein wählen (z. B. 10 Minuten), sonst sperrt YouTube.

Anime: siehe [04-anime.md](04-anime.md#anime-trailer-optional).

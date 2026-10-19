# 3. Download & *arr

Reihenfolge: SABnzbd → Prowlarr → Sonarr/Radarr/Lidarr → Jellyseerr.

## SABnzbd (8080)

- Usenet-Provider eintragen.
- Ordner: unfertig `/data/downloads/incomplete`, fertig `/data/downloads/complete`.
- Kategorien `tv`, `movies`, `music` anlegen.

## Prowlarr (9696)

- Indexer hinzufügen.
- Settings → Apps: Sonarr, Radarr, Lidarr mit deren API-Key verbinden – Prowlarr verteilt
  die Indexer dann automatisch.

## Sonarr (8989) / Radarr (7878)

- Root Folder: `/data/media/serien` bzw. `/data/media/filme`.
- Download Client: SABnzbd (Host `sabnzbd`, Port 8080, API-Key aus SABnzbd).
- Media Management: „Use Hardlinks instead of Copy“ an (Standard).

### Qualitätsprofil

Erfahrungswert: **1080p ohne Remux**. Remux-Releases sind 20–40 GB pro Film und bringen
auf den meisten Fernsehern keinen sichtbaren Vorteil. Im Profil die Remux-Qualitäten
abwählen, Obergrenze Bluray-1080p.

### Deutsche Releases: UmlautAdaptarrEx

Viele deutsche Releases heißen anders als der englische Titel (Umlaute, deutsche Titel).
UmlautAdaptarrEx sitzt als Proxy zwischen Sonarr/Radarr und den Indexern und sucht
zusätzlich mit den deutschen Titeln. Einrichtung über die Weboberfläche auf Port 5007.

## Lidarr (8686)

Root Folder `/music`, Download Client wie oben, Kategorie `music`.

## Jellyseerr (5055)

- Mit Jellyfin anmelden (Server `http://jellyfin:8096`), Bibliotheken synchronisieren.
- Radarr/Sonarr verbinden (Host `radarr` / `sonarr`).
- Benutzer aus Jellyfin importieren – dann kann jeder selbst wünschen.

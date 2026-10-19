# Jellyfin Media Stack

Ein komplettes Heimkino-Setup rund um **Jellyfin** – Filme, Serien, Anime, Live-TV mit 14 Tagen
Programm, Musik, Hörbücher, Bücher und Manga – als eine `docker-compose.yml` mit Anleitungen.

> Status: Vorlage / Entwurf. Pfade, Ports und Zugangsdaten an das eigene System anpassen.

## Was drin ist

| Bereich | Dienst | Port | Wofür |
|---|---|---|---|
| Mediaserver | **Jellyfin** | 8096 | Abspielen auf TV, Handy, Browser – mit Hardware-Transcoding |
| Wünsche | **Jellyseerr** | 5055 | Familie wünscht Filme/Serien, Radarr/Sonarr laden |
| Download | **SABnzbd** | 8080 | Usenet-Downloader |
| Indexer | **Prowlarr** | 9696 | Indexer zentral für alle *arr |
| Serien | **Sonarr** | 8989 | Serien suchen, laden, umbenennen |
| Filme | **Radarr** | 7878 | Filme suchen, laden, umbenennen |
| Musik | **Lidarr** | 8686 | Alben suchen und laden |
| Deutsch | **UmlautAdaptarrEx** | 5005–5007 | Deutsche Titel/Umlaute bei der Suche |
| Trailer | **Trailarr** | 7889 | Trailer lokal neben die Filme/Serien legen |
| Anime | **Shoko** + Plugin **Shokofin** | 8111 | AniDB-Erkennung, saubere Staffeln/Specials |
| Live-TV | **m3u-editor** (+ proxy, redis) | 36400 | IPTV-Liste filtern, Logos, EPG-Zuordnung |
| EPG | **epg-grabber** (iptv-org/epg) | – | 14 Tage Programm von MagentaTV |
| Musik-Streaming | **Navidrome** | 4533 | Subsonic-Server für Musik-Apps |
| Hörbücher | **Audiobookshelf** | 8000 | Hörbücher + Podcasts mit App |
| Bücher/Manga | **Kavita** | 5000 | Lesen im Browser/App |
| Manga-Download | **Suwayomi** | 8081 | Manga-Quellen abonnieren → Kavita |
| YouTube | **Pinchflat** | 8945 | YouTube-Kanäle abonnieren und archivieren |

```
                 ┌──────────── Jellyseerr (Wünsche)
                 ▼
Prowlarr ──► Sonarr / Radarr / Lidarr ──► SABnzbd ──► /data/downloads
                 │  (Hardlink, kein Kopieren)               │
                 ▼                                          │
            /data/media  ◄──────────────────────────────────┘
                 │            Trailarr legt Trailer daneben
                 ▼
             Jellyfin ◄── Shoko/Shokofin (Anime)
                 ▲
                 └── m3u-editor ◄── IPTV-Liste + EPG (MagentaTV 14 Tage + epgshare01)
```

## Schnellstart

```bash
sudo mkdir -p /opt/media-stack && cd /opt/media-stack
git clone <dieses-repo> .
cp .env.example .env && nano .env        # Pfade, Passwörter
docker compose up -d
```

Danach die Dienste in dieser Reihenfolge einrichten:

1. [Grundlagen: Ordner, Rechte, Hardlinks](docs/01-grundlagen.md)
2. [Jellyfin](docs/02-jellyfin.md)
3. [Download & *arr](docs/03-arr.md)
4. [Anime mit Shoko](docs/04-anime.md)
5. [Live-TV mit 14 Tagen EPG](docs/05-live-tv.md)
6. [Trailer](docs/06-trailer.md)
7. [Musik, Hörbücher, Bücher, YouTube](docs/07-weitere-medien.md)
8. [Updates, Backups, Fernzugriff](docs/08-betrieb.md)
9. [Apps für Fernseher und Handy](docs/09-clients.md)

## Hardware (Beispiel)

Läuft hier in einem Proxmox-LXC (Debian, Docker) mit Intel-GPU fürs Transcoding.
Medien auf mehreren Platten; ein gemeinsamer `/data`-Mount hält Downloads und Medien
auf demselben Dateisystem, damit Hardlinks funktionieren.

## Lizenz

Die Anleitungen und Skripte: MIT. Die einzelnen Dienste haben ihre eigenen Lizenzen.

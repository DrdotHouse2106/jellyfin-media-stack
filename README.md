# Jellyfin Media Stack

[![Spendier mir einen Kaffee](https://img.shields.io/badge/☕_Spendier_mir_einen_Kaffee-PayPal-0070ba?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/DrdotHouse)

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

## 📺 Die passende App: Quallenkino

Für den Fernseher gibt es mit **Quallenkino** einen eigenen Jellyfin-Client, der genau auf dieses
Setup abgestimmt ist – Startseite mit großem Infobereich und Trailer,
„Weiterschauen“, Empfehlungen mit Begründung („Weil du … geschaut hast“), **Live-TV mit
Programmführer und Darstellern**, „Heute im TV für dich“, „Top 10 bei euch“, Welten
(Filmreihen/Studios), Wünschen über Jellyseerr direkt aus der App und ein Bildschirmschoner
mit Teasern. Ton und Untertitel werden automatisch passend gewählt (Deutsch bevorzugt).

| Gerät | Download |
|---|---|
| Fire TV, Android TV, Google TV | [Quallenkino für Android TV](https://github.com/DrdotHouse2106/Jellyfin-TV-Client/releases/latest) |
| LG-Fernseher (webOS) | [Quallenkino für webOS](https://github.com/DrdotHouse2106/Quallenkino-webOS/releases/latest) |

Die Empfehlungs- und Live-TV-Reihen brauchen das Server-Plugin
[Quallenkino](https://github.com/DrdotHouse2106/Lokal-Vorschlag-Jellyfin) (Quallenkinoplugin für Jellyfin, früher „Local Recommendations“/LocalRecs). Mehr dazu und zu
anderen Apps: [docs/09-clients.md](docs/09-clients.md).

## Schnellstart

```bash
sudo mkdir -p /opt/media-stack && cd /opt/media-stack
git clone <dieses-repo> .
cp .env.example .env && nano .env        # Pfade, Passwörter
docker compose up -d
```

Danach die Dienste in dieser Reihenfolge einrichten:

1. [Grundlagen: Ordner, Rechte, Hardlinks](docs/01-grundlagen.md)
2. [Jellyfin und Plugins](docs/02-jellyfin.md) – welche Plugins und Einstellungen es für diesen Aufbau braucht
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

## ☕ Unterstützen

In diesem Setup stecken viele Abende: ausprobieren, Fehler suchen, Anleitungen schreiben,
dazu Server, Testgeräte und KI-Werkzeuge. Wenn es dir Zeit gespart hat, freue ich mich über
einen Kaffee – freiwillig, ohne Support-Anspruch, einfach eine nette Geste:

[![Spendier mir einen Kaffee](https://img.shields.io/badge/☕_Spendier_mir_einen_Kaffee-PayPal-0070ba?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/DrdotHouse)

### 🎮 Auch eine Zocker-Ader?

Dann ist vielleicht mein anderes Projekt genau das Richtige für dich: **[ZockerDB](https://zockerdb.de)** –
deine Spielesammlung an einem Platz. Spiele, Konsolen und Zubehör erfassen (auch per Barcode-Scan mit
dem Handy), bewerten und verwalten, mit Preisverlauf, Editionen und PAL/USK-Angaben. Direkt auf
[zockerdb.de](https://zockerdb.de) nutzen oder als [ZockerDB Basis](https://github.com/DrdotHouse2106/ZockerDBBasis) auf dem eigenen Server hosten.

## Lizenz

Die Anleitungen und Skripte: MIT. Die einzelnen Dienste haben ihre eigenen Lizenzen.

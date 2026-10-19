# 2. Jellyfin

Weboberfläche: `http://SERVER-IP:8096` – Assistent durchklicken, Bibliotheken anlegen:

| Bibliothek | Typ | Ordner im Container |
|---|---|---|
| Filme | Filme | `/data/media/filme` |
| Serien | Serien | `/data/media/serien` |
| Anime | Serien | über Shokofin (siehe [04](04-anime.md)) |

## Hardware-Transcoding (Intel/AMD)

1. Auf dem Host: `ls -l /dev/dri` → `renderD128` muss existieren.
   In einem Proxmox-LXC das Gerät an den Container durchreichen.
2. `RENDER_GID` in der `.env` auf die Gruppe von `/dev/dri/renderD128` setzen.
3. Bei manchen Systemen braucht der Benutzer im Container zusätzlich die Gruppe `video` –
   dafür liegt [`scripts/jellyfin/gpu.sh`](../scripts/jellyfin/gpu.sh) bei. Nach
   `config/jellyfin/custom-cont-init.d/` kopieren; der linuxserver-Container führt es beim Start aus.
4. Jellyfin → Dashboard → Wiedergabe → Transcoding: *Intel QuickSync (QSV)* oder *VAAPI*,
   Gerät `/dev/dri/renderD128`, passende Codecs anhaken.

## Empfehlenswerte Plugins

| Plugin | Wofür |
|---|---|
| **Shokofin** | Anime aus Shoko (siehe [04](04-anime.md)) |
| **Intro Skipper** | „Intro überspringen“-Knopf |
| **LocalRecs** ([eigenes Plugin](https://github.com/DrdotHouse2106/Lokal-Vorschlag-Jellyfin)) | Vorschläge „Weil du … geschaut hast“, „Heute im TV für dich“, „Top 10 bei euch“, Welten (Filmreihen/Studios) |

## Sprache

- Benutzer → Wiedergabe: bevorzugte Audiosprache **Deutsch**, Untertitel „Intelligent“.
- Bibliotheken: Metadatensprache Deutsch, Land Deutschland.

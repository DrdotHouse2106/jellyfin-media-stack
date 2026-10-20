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

## Plugins

So ist der Server hier eingerichtet. Ohne die markierten Plugins (★) fehlen in Jellyfin Web und in
der Handy-App die Startseite im Quallenkino-Stil, die Empfehlungen und die Zusatzreihen, und Quallenkino zeigt
weniger an.

### 1. Repositories hinzufügen

Dashboard → Plugins → Repositories → **+**. Danach im Katalog installieren und Jellyfin neu starten.

| Name | URL |
|---|---|
| Jellyfin Stable | `https://repo.jellyfin.org/files/plugin/manifest.json` (ist schon da) |
| DrdotHouse Plugins | `https://raw.githubusercontent.com/DrdotHouse2106/Jellyfin-Plugins/main/manifest.json` |
| File Transformation (IAmParadox) | `https://www.iamparadox.dev/jellyfin/plugins/manifest.json` |
| Jellyfin Enhanced | `https://raw.githubusercontent.com/n00bcodr/jellyfin-plugins/main/12/manifest.json` |
| Intro Skipper | `https://intro-skipper.org/manifest.json` |
| JellyBridge | `https://raw.githubusercontent.com/kinggeorges12/JellyBridge/refs/heads/main/manifest.json` |
| Shoko | `https://raw.githubusercontent.com/ShokoAnime/Shokofin/metadata/dev/manifest.json` |

### 2. Plugins

| Plugin | Repository | Wofür |
|---|---|---|
| ★ **File Transformation** | IAmParadox | Grundlage: erlaubt anderen Plugins, die Weboberfläche zu erweitern. **Zuerst installieren.** |
| ★ **Quallenkinoplugin für Jellyfin** (früher Local Recommendations / LocalRecs) | DrdotHouse | Empfehlungen „Weil du … geschaut hast“, „Heute im TV für dich“, „Top 10 bei euch“, Welten, Darsteller im Live-TV, Erinnerungen im Kalender, Aufnehmen, „Wer schaut?“ mit Profilbildern, eigener EPG-Anbieter – und die **Startseite im Quallenkino-Stil** für Jellyfin Web und die Handy-Apps. Quellcode: [Lokal-Vorschlag-Jellyfin](https://github.com/DrdotHouse2106/Lokal-Vorschlag-Jellyfin) |
| ★ **Home Screen Sections** | IAmParadox | Zusätzliche Reihen auf der Startseite (Weiterschauen, Kürzlich hinzugefügt, Genres, „Weil du … geschaut hast“). Das Quallenkinoplugin meldet dort seine Reihen an; Quallenkino liest sie auch. |
| **Plugin Pages** | IAmParadox | Eigene Seiten von Plugins im Benutzermenü (wird von Home Screen Sections genutzt). |
| **Jellyfin Enhanced** | Jellyfin Enhanced | Qualitäts- und Bewertungs-Abzeichen auf den Kacheln, Zufallsknopf, Pausenbildschirm, Kalender, Lesezeichen, „Wo sonst streamen“, Jellyseerr-Suche. |
| **Jellyfin Remote** | DrdotHouse | Handy als Fernbedienung für Quallenkino und andere Jellyfin-Apps. Quellcode: [Jellyfin-Remote](https://github.com/DrdotHouse2106/Jellyfin-Remote) |
| **Intro Skipper** | Intro Skipper | Erkennt Intro, Abspann, Rückblick und Vorschau; „Überspringen“ in allen Apps. |
| **JellyBridge** | JellyBridge | Verbindet Jellyfin mit Jellyseerr (Wünsche und Entdecken). |
| **Shoko** (Shokofin) | Shoko | Anime aus Shoko (siehe [04](04-anime.md)). |
| **TMDb Box Sets** | Jellyfin Stable | Legt Filmreihen automatisch als Sammlungen an – Grundlage für „Nächster Teil nach …“. |
| **Trakt** | Jellyfin Stable | Gesehen-Status mit Trakt abgleichen (pro Benutzer anmelden). |
| **Open Subtitles** | Jellyfin Stable | Untertitel herunterladen (Konto bei opensubtitles.com nötig). |
| **OMDb**, **TMDb**, **Studio Images**, **AudioDB**, **MusicBrainz**, **ListenBrainz Similarity Provider** | mitgeliefert / Stable | Metadaten, Studio-Logos, Musik. |

### 3. Einstellungen, auf die es ankommt

**Quallenkinoplugin für Jellyfin** (Dashboard → Plugins → Quallenkinoplugin für Jellyfin):
- Reiter *Einstellungen*, Abschnitt *Jellyfin Web*: **„Startseite im Quallenkino-Stil“** und **„Quallenkino-Farben“** einschalten, dazu „Wer schaut?“ und „Profilbilder aus Figuren wählen“.
  Wirkt ohne Neustart; jeder Benutzer kann unten auf der Startseite zur klassischen Ansicht wechseln.
- Live-TV-Reihe an, Titel z. B. „Heute im TV für dich“; Welten-Liste kommt aus
  [Jellyfin-Welten](https://github.com/DrdotHouse2106/Jellyfin-Welten) (Voreinstellung).
- Für die Darsteller im Live-TV die XMLTV-Datei aus [05](05-live-tv.md) eintragen (Reiter *Startseite*, „XMLTV-Quelle für Darsteller“).
- Reiter *Fernsehprogramm*: eigener EPG-Anbieter „LocalRecs EPG“ statt des XMLTV-Anbieters von Jellyfin (Film/Serie über Regeln statt Filmkategorien, siehe [05](05-live-tv.md)).

**Home Screen Sections** (Dashboard → Plugins → Home Screen Sections):
- Plugin an, *Lazy Load* aus, *Benutzer dürfen anpassen* an.
- Eingeschaltete Reihen hier: Weiterschauen + Als Nächstes (zusammen), Quallenkinoplugin Live-TV / Serien /
  Filme, Kürzlich hinzugefügt Filme und Serien, „Weil du … geschaut hast“, Nochmal ansehen, Genre,
  Regie, Darsteller. Den Rest aus.

**Intro Skipper**:
- Erkennung von Intro, Abspann, Rückblick, Vorschau und Werbung an, *Media Segments aktualisieren* an.
- Automatisches Überspringen aus – den Knopf zeigen die Apps selbst (Quallenkino springt nach 5 s).

**Jellyfin Enhanced**: Abzeichen (Qualität, Bewertung), Zufallsknopf, Pausenbildschirm, Kalender,
Lesezeichen, Jellyseerr an; das eingebaute Theme-Menü aus (die Farben kommen vom Quallenkinoplugin).

**JellyBridge**: Jellyseerr-Adresse (z. B. `http://jellyseerr:5055/`) und API-Key aus Jellyseerr eintragen.

**Jellyfin Remote**: *Symbol in der Kopfzeile* an, *nur auf Handys und Tablets* an,
öffentliche Adresse eintragen, wenn die Fernbedienung auch von unterwegs gehen soll.

### 4. Hinweise

- Nach jedem Plugin-Update Jellyfin neu starten und die Weboberfläche einmal neu laden.
- **iPhone-App zeigt die neuen Reihen nicht?** Die App hält alte Dateien im Zwischenspeicher.
  Server entfernen hilft nicht – App löschen und neu installieren.
- Das Feld *Dashboard → Allgemein → Branding → Eigenes CSS* leer lassen, sonst überdeckt es
  die Farben des Quallenkinoplugins.

## Sprache

- Benutzer → Wiedergabe: bevorzugte Audiosprache **Deutsch**, Untertitel „Intelligent“.
- Bibliotheken: Metadatensprache Deutsch, Land Deutschland.

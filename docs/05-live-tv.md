# 5. Live-TV mit 14 Tagen EPG

```
IPTV-Anbieter (M3U)  ──►  m3u-editor  ──►  Jellyfin (Tuner „M3U“ + Guide „XMLTV“)
                             ▲
MagentaTV ─► epg-grabber ─┐  │
                          ├─► enrich_epg.py ─► epg_DE1_enriched.xml.gz
epgshare01 (DE1) ─────────┘         └──────────► Quallenkinoplugin (Darsteller, Film-Merkmale)
```

## m3u-editor (36400)

1. Playlist: M3U-URL des Anbieters eintragen.
2. Gewünschte Sender aktivieren, Namen/Logos/Reihenfolge anpassen.
3. EPG hinzufügen: URL der angereicherten Datei (siehe unten),
   `http://SERVER-IP:36400/storage/epg/epg_DE1_enriched.xml.gz`, Sync z. B. `0 */6 * * *`.
4. Sender mit dem EPG verknüpfen (automatische Zuordnung, Rest von Hand).
5. Die Playlist liefert zwei Adressen: M3U und `…/epg.xml` – beide kommen in Jellyfin.

Wichtig: `DEFAULT_EPG_DAYS=14` in der Compose-Datei. Ohne gibt m3u-editor nur 7 Tage weiter.
Nach einer Änderung den Ausgabe-Cache leeren:
`docker exec m3u-editor php artisan app:clear-playlist-epg-files --force`

## Jellyfin

- Dashboard → Live-TV → Tuner: **M3U-Tuner** mit der M3U-Adresse des m3u-editors.
- TV-Programm-Anbieter: **XMLTV** mit der `epg.xml`-Adresse.
- Einstellung **Guide-Tage: 14** (Maximum; Standard ist 7).
- Geplante Aufgabe „TV-Programm aktualisieren“ zusätzlich auf feste Uhrzeiten legen
  (z. B. 06:15 und 18:15) – nur das 24-h-Intervall ist bei uns einmal ausgefallen.

## 14 Tage Programm: epg-grabber

Freie deutsche EPG-Quellen wie epgshare01 reichen nur 3–4 Tage. Das Projekt
[iptv-org/epg](https://github.com/iptv-org/epg) liest Programmseiten aus; **MagentaTV**
liefert 14 Tage für über 300 Sender, mit Beschreibung, Bildern, Regie und Darstellern.

Einrichten:

```bash
cd /opt/media-stack/epg-grabber
git clone https://github.com/iptv-org/epg.git epg
cd epg && git apply --ignore-whitespace ../magenta-actors.patch   # Darsteller mitnehmen
cd .. && docker compose up -d epg-grabber
```

- `run.sh` holt alle 12 h das Programm → `magenta.xml` (ca. 10 s für 115 Sender).
- `magenta.channels.xml` ordnet MagentaTV-Sender (`site_id`) den EPG-IDs zu, die der
  m3u-editor für die eigenen Sender nutzt (`xmltv_id`, hier die IDs von epgshare01 DE1).
  Alle verfügbaren Sender: `epg/sites/web.magentatv.de/web.magentatv.de.channels.xml`.
- `magenta-actors.patch`: Die Original-Konfiguration übernimmt nur Regie/Produktion;
  die API liefert aber auch Darsteller.

## Zusammenführen + Bundesliga: enrich_epg.py

[`scripts/epg-enrich/enrich_epg.py`](../scripts/epg-enrich/enrich_epg.py), per Cron 10 Minuten
vor dem EPG-Sync des m3u-editors:

```
50 3,9,15,21 * * * /usr/bin/python3 /opt/media-stack/scripts/epg-enrich/enrich_epg.py --out /opt/media-stack/config/m3u-editor/storage/epg/epg_DE1_enriched.xml.gz >> /opt/media-stack/scripts/epg-enrich/enrich.log 2>&1
```

- Lädt epgshare01 DE1 und ersetzt für jeden Sender mit MagentaTV-Daten dessen Sendungen
  (doppelte entfernt). Sender ohne MagentaTV bleiben bei DE1.
- Ist `magenta.xml` älter als 48 h, nimmt es nur DE1 (Log: „ohne MagentaTV“).
- Benennt die Sky-Sport-Bundesliga-Einzelkanäle („Live: BL“) anhand des Stadions mit der Paarung.
- Schreibt atomar; bei Fehlern bleibt die letzte Datei liegen.

## Darsteller in Jellyfin

Weder m3u-editor noch Jellyfin übernehmen Darsteller aus XMLTV. Das Quallenkinoplugin (früher LocalRecs) liest
sie deshalb direkt aus der Datei – dafür ist sie in den Jellyfin-Container unter
`/epg-source` eingehängt.

## Film oder Serie: EPG-Anbieter „LocalRecs EPG“ (in Erprobung)

Der XMLTV-Anbieter von Jellyfin macht jede Sendung zum Film, sobald eine ihrer Kategorien in der
Liste „Filmkategorien“ steht (z. B. „Komödie“). Staffel und Folge gehen dann verloren, Aufnahmen
landen unter `Filme/`. Das Quallenkinoplugin bringt ab 12.26 einen eigenen Anbieter mit (Reiter
*Fernsehprogramm*): Serie über die Folgennummer, Film nur mit Mindestlänge und Regie, IMDb oder
Kategorie „Spielfilm“. Sendungen und Sender-IDs kommen weiter vom m3u-editor, Regie, Jahr und IMDb
ab 12.27 aus der Datei unter `/epg-source`.

Umstellung: Reiter *Fernsehprogramm* → bisherigen XMLTV-Anbieter zum Übernehmen wählen →
„LocalRecs EPG einrichten“ → „Regeln testen“. Den alten Anbieter erst unter Dashboard → Live-TV
löschen, wenn die Einordnung stimmt.

# 1. Grundlagen: Ordner, Rechte, Hardlinks

## Ordnerstruktur

```
/opt/media-stack/            ← dieses Repo
  docker-compose.yml
  .env                       ← Pfade + Passwörter (nicht committen)
  config/<dienst>/           ← Einstellungen/Datenbanken aller Container
  epg-grabber/               ← EPG-Abruf (siehe 05)
  scripts/                   ← Hilfsskripte (Cron)

/data/                       ← DATA_DIR – EIN Dateisystem
  downloads/                 ← SABnzbd
  media/filme/               ← Radarr
  media/serien/              ← Sonarr
  anime/                     ← Shoko/Sonarr
  musik/ hoerbuecher/ buecher/ manga/ youtube/
```

## Warum ein gemeinsamer Datenordner?

Sonarr/Radarr verschieben fertige Downloads in die Bibliothek. Liegen Downloads und Medien
im **selben Mount** (`/data`) und auf **demselben Dateisystem**, wird ein *Hardlink* angelegt:
sofort fertig, kein doppelter Platz, und der Download kann weiter geseedet werden.
Getrennte Mounts (`/downloads` und `/movies`) erzwingen dagegen Kopieren.

Tipp: In allen Containern dieselben Pfade verwenden (`/data/...`). Dann braucht es nirgends
„Remote Path Mappings“ – auch Trailarr findet die Ordner direkt.

## Rechte

Alle Container laufen als `PUID`/`PGID` aus der `.env` (meist 1000). Die Medienordner
müssen diesem Benutzer gehören:

```bash
sudo chown -R 1000:1000 /data
```

## Mehrere Platten

Geht auch ohne RAID/MergerFS: zusätzliche Platten als weitere Ordner einhängen und in
Sonarr/Radarr als zusätzliche „Root Folder“ anlegen. Jede Platte braucht dann aber ihren
eigenen Download-Ordner auf derselben Platte, sonst klappen Hardlinks dort nicht.

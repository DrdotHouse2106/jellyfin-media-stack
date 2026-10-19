# 8. Updates, Backups, Fernzugriff

## Updates

[`scripts/update_docker.sh`](../scripts/update_docker.sh) zieht neue Images (mit Wiederholung,
höchstens 2 parallel wegen Rate-Limits), startet geänderte Container neu und räumt alte Images auf.

```
0 4 * * 0 /opt/media-stack/scripts/update_docker.sh >> /opt/media-stack/update_docker.log 2>&1
```

Vorsicht bei `:latest`: Ein Update kann Datenbanken migrieren. Vor großen Versionssprüngen
(z. B. Jellyfin) ein Backup machen und die Release Notes lesen.

## Backups

Wichtig ist nur `config/` – Medien lassen sich neu laden, Einstellungen, Gesehen-Status und
Datenbanken nicht. Am einfachsten: Container stoppen, `config/` packen, starten.
Unter Proxmox reicht ein regelmäßiger Snapshot/Backup des LXC.

Vor Änderungen an `docker-compose.yml` eine Kopie anlegen
(`cp docker-compose.yml docker-compose.yml.bak-$(date +%Y%m%d)`).

## Fernzugriff

Möglichkeiten, von unterwegs auf Jellyfin zu kommen:

| Weg | Vorteil | Nachteil |
|---|---|---|
| **VPN** (WireGuard, Tailscale) | nichts offen im Internet | App/VPN auf jedem Gerät |
| **Reverse Proxy** mit eigener Domain + HTTPS (Caddy, Nginx Proxy Manager, Traefik) | funktioniert überall, auch auf Fernsehern bei Freunden | Port offen, Updates wichtig |
| Reverse Proxy auf einem **gemieteten Server** (z. B. bei DS-Lite ohne eigene IPv4) | geht auch ohne öffentliche IPv4 | zusätzlicher Umweg, langsamer als im Heimnetz |

Bei wechselnder IP (v. a. IPv6) braucht es DynDNS. Die meisten DNS-Anbieter haben dafür eine API;
ein kleines Skript per Cron prüft die aktuelle Adresse und aktualisiert den Eintrag nur bei Änderung.

Im Heimnetz sollten Apps direkt die lokale Adresse nutzen – über die Domain läuft jeder Film
sonst einmal durchs Internet und zurück.

Nicht ins Internet stellen: die *arr-Dienste, SABnzbd, Prowlarr, m3u-editor, Shoko.

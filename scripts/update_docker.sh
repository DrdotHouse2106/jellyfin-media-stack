#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export COMPOSE_PARALLEL_LIMIT=2   # nicht alles gleichzeitig ziehen (lscr.io Rate-Limit)
cd "${STACK_DIR:-/opt/media-stack}" || exit 1

echo "=== $(date) ==="

# Docker-Bilder aktualisieren (mit Wiederholung bei Fehlern)
for i in 1 2 3; do
    docker compose pull && break
    echo "Pull fehlgeschlagen (Versuch $i), warte 60s..."
    sleep 60
done

# Container neu starten
docker compose up -d

# Unnötigen Datenmüll entfernen
docker image prune -f

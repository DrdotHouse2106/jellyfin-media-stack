#!/bin/sh
# EPG von MagentaTV über iptv-org/epg holen (14 Tage), alle 12 Stunden.
# Ergebnis: /work/magenta.xml – enrich_epg.py führt es mit epgshare01 zusammen.
cd /work/epg || exit 1
if [ ! -d node_modules ]; then
  npm ci --ignore-scripts --no-audit --no-fund > /work/npm.log 2>&1 || { echo "$(date '+%F %T') FEHLER: npm ci" >> /work/grab.log; sleep 3600; exit 1; }
fi
while true; do
  rm -f /work/magenta.tmp.xml
  if npm run grab --- --channels=/work/magenta.channels.xml --days=14 --maxConnections=3 \
       --output=/work/magenta.tmp.xml > /work/grab-letzter-lauf.log 2>&1 && [ -s /work/magenta.tmp.xml ]; then
    mv /work/magenta.tmp.xml /work/magenta.xml
    echo "$(date '+%F %T') OK: $(grep -c '<programme' /work/magenta.xml) Sendungen" >> /work/grab.log
  else
    echo "$(date '+%F %T') FEHLER, siehe grab-letzter-lauf.log – letzte Datei bleibt" >> /work/grab.log
  fi
  sleep 43200
done

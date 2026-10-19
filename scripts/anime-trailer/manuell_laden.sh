#!/bin/bash
# Von Hand ausgewählte Anime-Trailer/Teaser laden – für Serien, die Trailarr nicht eindeutig zuordnen kann
# (z. B. mehrere Shoko-Einträge in einem Ordner). Liste: manuell.txt, eine Zeile pro Video:
#   <Shoko-Serien-ID> <trailer|teaser> <YouTube-ID> <Name>
# Ziel: $TRAILER_ROOT/shoko-<ID>/ – anime_trailer_link.py ordnet diese Ordner direkt per Shoko-ID zu.
set -u
TRAILER_ROOT=${TRAILER_ROOT:-/anime-trailer}
LIST=${1:-$(dirname "$0")/manuell.txt}
grep -v '^\s*#' "$LIST" | while read -r sid kind yt name; do
  [ -z "${sid:-}" ] && continue
  dir="$TRAILER_ROOT/shoko-$sid"; out="$dir/$name-$kind.mkv"
  [ -s "$out" ] && { echo "vorhanden: $out"; continue; }
  mkdir -p "$dir"
  # yt-dlp aus dem Trailarr-Container (dort aktuell gehalten); TRAILER_ROOT muss dort gleich gemountet sein
  docker exec trailarr yt-dlp --no-warnings --no-playlist -q \
    -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mkv \
    -o "$out" "https://www.youtube.com/watch?v=$yt" </dev/null \
    && echo "OK $sid $kind $yt" || echo "FEHLER $sid $kind $yt"
  sleep 60   # YouTube nicht drängen
done
chown -R "${PUID:-1000}:${PGID:-1000}" "$TRAILER_ROOT"

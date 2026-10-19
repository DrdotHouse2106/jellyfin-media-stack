#!/usr/bin/env python3
"""Anime-Trailer aus Trailarr an die Serien im Shokofin-VFS hängen.

Zuordnung ohne Namensvergleich:
  Trailarr-Download (Profil "Anime Trailers"/"Anime Teaser") -> Trailarr-Eintrag -> echter Serienordner
  echter Serienordner <- Ziele der Episoden-Links im VFS-Serienordner
Verknüpft wird nur, wenn ein echter Ordner genau zu einem VFS-Ordner gehört und umgekehrt,
oder wenn zuordnung.txt den Fall ausdrücklich regelt. Videos in sperrliste.txt werden nie verknüpft.

Von Hand ausgewählte Videos liegen in <TRAILER_ROOT>/shoko-<Shoko-ID>/ und gehören genau
zu dem VFS-Eintrag mit dieser Shoko-Serien-ID.

  anime_trailer_link.py            Probelauf: schreibt nur bericht.txt
  anime_trailer_link.py --apply    verknüpft und lässt Jellyfin die geänderten Serien neu einlesen
"""
import json
import os
import sqlite3
import sys
import urllib.request
from collections import defaultdict

# Anpassen: Stack-Ordner und die Pfade, wie sie Trailarr sieht (am besten gleiche Pfade wie auf dem Host)
STACK = os.environ.get("STACK_DIR", "/opt/media-stack")
BASE = os.path.join(STACK, "scripts/anime-trailer")
TRAILARR_DB = os.path.join(STACK, "config/trailarr/trailarr.db")
JELLYFIN_DB = os.path.join(STACK, "config/jellyfin/data/data/jellyfin.db")
VFS_HOST = os.path.join(STACK, "config/jellyfin/data/Shokofin/VFS")
VFS_CONTAINER = "/config/data/Shokofin/VFS"
ANIME_ROOT = os.environ.get("ANIME_ROOT", "/anime/")              # Anime-Ordner, wie Trailarr ihn sieht
TRAILER_ROOT = os.environ.get("TRAILER_ROOT", "/anime-trailer/")  # custom_folder der Trailarr-Anime-Profile
PROFILES = ("Anime Trailers", "Anime Teaser")
JELLYFIN = "http://localhost:8096"

APPLY = "--apply" in sys.argv


def read_list(name):
    """Zeilen einer Steuerdatei ohne Kommentare."""
    path = os.path.join(BASE, name)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [l.split("#")[0].strip() for l in f if l.split("#")[0].strip()]


def series_folder(target):
    """<ANIME_ROOT>/<Serie>/... -> <ANIME_ROOT>/<Serie>"""
    if not target.startswith(ANIME_ROOT):
        return None
    return ANIME_ROOT + target[len(ANIME_ROOT):].split("/")[0]


def shoko_id(vfs_dir):
    """'Name [Shoko Series=238]' -> '238'"""
    marker = "[Shoko Series="
    if marker not in vfs_dir:
        return None
    return vfs_dir.split(marker, 1)[1].split("]", 1)[0]


def scan_vfs():
    """VFS-Serienordner -> echte Serienordner (aus den Episoden-Links)."""
    vfs_to_src = {}
    for lib in os.listdir(VFS_HOST):
        lib_path = os.path.join(VFS_HOST, lib)
        if not os.path.isdir(lib_path):
            continue
        for show in os.listdir(lib_path):
            show_path = os.path.join(lib_path, show)
            if not os.path.isdir(show_path):
                continue
            sources = set()
            for root, dirs, files in os.walk(show_path):
                if os.path.basename(root) == "trailers":
                    continue
                for f in files:
                    p = os.path.join(root, f)
                    if os.path.islink(p):
                        src = series_folder(os.readlink(p))
                        if src:
                            sources.add(src)
            vfs_to_src[show_path] = sources
    return vfs_to_src


def trailarr_downloads():
    con = sqlite3.connect(f"file:{TRAILARR_DB}?mode=ro", uri=True)
    rows = con.execute(
        """select m.txdb_id, m.title, m.folder_path, d.path, d.youtube_id, d.duration, c.filter_name
           from download d join media m on m.id = d.media_id
           join trailerprofile p on p.id = d.profile_id
           join customfilter c on c.id = p.customfilter_id
           where d.file_exists = 1 and c.filter_name in (?, ?)""",
        PROFILES,
    ).fetchall()
    con.close()
    out = []
    for txdb, title, folder, path, yt, duration, profile in rows:
        if not path or not path.startswith(TRAILER_ROOT) or not os.path.exists(path):
            continue
        out.append({
            "tvdb": str(txdb), "title": title, "folder": (folder or "").rstrip("/"),
            "path": path, "youtube": yt or "", "duration": duration or 0, "profile": profile,
        })
    return out


def jellyfin_request(path, method="GET"):
    con = sqlite3.connect(f"file:{JELLYFIN_DB}?mode=ro", uri=True)
    token = con.execute("select AccessToken from ApiKeys limit 1").fetchone()[0]
    con.close()
    req = urllib.request.Request(JELLYFIN + path, method=method,
                                 headers={"Authorization": f'MediaBrowser Token="{token}"'})
    body = urllib.request.urlopen(req, timeout=60).read()
    return json.loads(body) if body else None


def refresh_series(show_paths):
    """Geänderte Serien in Jellyfin neu einlesen (nur diese, keine ganze Bibliothek)."""
    wanted = {p.replace(VFS_HOST, VFS_CONTAINER, 1) for p in show_paths}
    items = jellyfin_request("/Items?Recursive=true&IncludeItemTypes=Series&Fields=Path")["Items"]
    for item in items:
        if item.get("Path") in wanted:
            jellyfin_request(f"/Items/{item['Id']}/Refresh?metadataRefreshMode=Default"
                             "&imageRefreshMode=Default&replaceAllMetadata=false", "POST")
            print("Jellyfin liest neu ein:", item["Name"])


def main():
    blocked = set(read_list("sperrliste.txt"))          # YouTube-IDs
    overrides = defaultdict(set)                          # TVDB-ID -> Shoko-Serien-IDs
    for line in read_list("zuordnung.txt"):               # Format: <TVDB-ID> <Shoko-ID>[,<Shoko-ID>...]
        tvdb, ids = line.split(None, 1)
        overrides[tvdb].update(i.strip() for i in ids.split(","))

    vfs_to_src = scan_vfs()
    src_to_vfs = defaultdict(set)
    for show, sources in vfs_to_src.items():
        for s in sources:
            src_to_vfs[s].add(show)

    plan = defaultdict(list)      # VFS-Ordner -> Trailer
    report = []
    for dl in sorted(trailarr_downloads(), key=lambda d: d["title"]):
        line = f'{dl["title"]} | {dl["profile"]} | {int(dl["duration"])} s | https://youtu.be/{dl["youtube"]} | {dl["folder"]}'
        if dl["youtube"] in blocked:
            report.append(("GESPERRT", line, ""))
            continue
        shows = src_to_vfs.get(dl["folder"], set())
        if dl["tvdb"] in overrides:
            targets = [s for s in shows if shoko_id(os.path.basename(s)) in overrides[dl["tvdb"]]]
            status = "ZUORDNUNG" if targets else "ZUORDNUNG OHNE TREFFER"
        elif len(shows) == 1 and vfs_to_src[next(iter(shows))] == {dl["folder"]}:
            targets, status = list(shows), "EINDEUTIG"
        elif not shows:
            targets, status = [], "KEINE SERIE IM VFS"
        else:
            targets, status = [], "UNKLAR"
        names = " / ".join(sorted(os.path.basename(s) for s in (targets or shows)))
        report.append((status, line, names))
        for t in targets:
            plan[t].append(dl)

    # Von Hand ausgewählte Videos: <TRAILER_ROOT>/shoko-<Shoko-ID>/ gehört genau zu dem Eintrag mit dieser ID
    by_shoko = {shoko_id(os.path.basename(s)): s for s in vfs_to_src}
    for folder in sorted(os.listdir(TRAILER_ROOT)):
        if not folder.startswith("shoko-"):
            continue
        sid = folder[len("shoko-"):]
        show = by_shoko.get(sid)
        for name in sorted(os.listdir(os.path.join(TRAILER_ROOT, folder))):
            if not name.endswith((".mkv", ".mp4", ".webm")):
                continue
            path = os.path.join(TRAILER_ROOT, folder, name)
            line = f"{name} | von Hand | Shoko-ID {sid}"
            if show is None:
                report.append(("MANUELL OHNE TREFFER", line, ""))
                continue
            report.append(("MANUELL", line, os.path.basename(show)))
            plan[show].append({"path": path})

    # Bericht
    os.makedirs(BASE, exist_ok=True)
    order = ["EINDEUTIG", "MANUELL", "ZUORDNUNG", "UNKLAR", "MANUELL OHNE TREFFER", "ZUORDNUNG OHNE TREFFER", "KEINE SERIE IM VFS", "GESPERRT"]
    with open(os.path.join(BASE, "bericht.txt"), "w", encoding="utf-8") as f:
        f.write(f"Modus: {'verknüpfen' if APPLY else 'Probelauf (nichts verknüpft)'}\n")
        for status in order:
            entries = [r for r in report if r[0] == status]
            if not entries:
                continue
            f.write(f"\n== {status} ({len(entries)})\n")
            for _, line, names in entries:
                f.write(f"{line}\n    -> {names or '-'}\n")
    print(f"Bericht: {os.path.join(BASE, 'bericht.txt')} ({len(report)} Trailer)")

    if not APPLY:
        return

    changed = set()
    for show in vfs_to_src:
        tdir = os.path.join(show, "trailers")
        want = {os.path.basename(d["path"]): d["path"] for d in plan.get(show, [])}
        # eigene alte Links entfernen, die nicht mehr gewollt sind
        if os.path.isdir(tdir):
            for f in os.listdir(tdir):
                p = os.path.join(tdir, f)
                if os.path.islink(p) and os.readlink(p).startswith(TRAILER_ROOT) and want.get(f) != os.readlink(p):
                    os.unlink(p)
                    changed.add(show)
        for name, target in want.items():
            p = os.path.join(tdir, name)
            if os.path.islink(p) and os.readlink(p) == target:
                continue
            os.makedirs(tdir, exist_ok=True)
            os.chown(tdir, 1000, 1000)
            os.symlink(target, p)
            os.lchown(p, 1000, 1000)
            changed.add(show)
        if os.path.isdir(tdir) and not os.listdir(tdir):
            os.rmdir(tdir)
    if changed:
        refresh_series(changed)
    print("Geänderte Serien:", len(changed))


if __name__ == "__main__":
    main()

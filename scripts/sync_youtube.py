#!/usr/bin/env python3
"""Sync the latest uploads from a YouTube channel into videos.json.

YouTube's RSS feed does not send CORS headers, so the browser cannot read it
directly. Instead this script runs at build time (locally or in the Pages
workflow) and writes a same-origin JSON file the page can fetch.

Usage: python3 scripts/sync_youtube.py
"""

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

CHANNEL_ID = "UC1DaZrN3ZI5BYf0hH6TRwgQ"
CHANNEL_URL = "https://www.youtube.com/@genai_practice"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
MAX_VIDEOS = 6

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "videos.json"

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (portfolio-sync)"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read()


def parse(xml_bytes: bytes):
    feed = ET.fromstring(xml_bytes)
    channel_title = (feed.findtext("atom:title", default="", namespaces=NS) or "").strip()

    videos = []
    for entry in feed.findall("atom:entry", NS):
        group = entry.find("media:group", NS)
        video_id = entry.findtext("yt:videoId", default="", namespaces=NS) or ""
        if not video_id:
            continue

        thumbnail = ""
        if group is not None:
            thumb = group.find("media:thumbnail", NS)
            if thumb is not None:
                thumbnail = thumb.get("url", "")

        views = None
        if group is not None:
            stats = group.find("media:community/media:statistics", NS)
            if stats is not None and stats.get("views"):
                try:
                    views = int(stats.get("views"))
                except ValueError:
                    pass

        videos.append(
            {
                "id": video_id,
                "title": (entry.findtext("atom:title", default="", namespaces=NS) or "").strip(),
                "published": entry.findtext("atom:published", default="", namespaces=NS) or "",
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": thumbnail or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
                "views": views,
            }
        )

    videos.sort(key=lambda v: v["published"], reverse=True)
    return channel_title, videos[:MAX_VIDEOS]


def main() -> int:
    try:
        channel_title, videos = parse(fetch(FEED_URL))
        if not videos:
            raise ValueError("feed contained no videos")
    except Exception as exc:  # noqa: BLE001 - keep the existing file on any failure
        print(f"warning: could not sync YouTube feed ({exc})", file=sys.stderr)
        if OUT.exists():
            print("keeping existing videos.json", file=sys.stderr)
            return 0
        OUT.write_text(
            json.dumps({"channel": {"title": "GenAI Practice", "url": CHANNEL_URL}, "videos": []}, indent=2)
            + "\n",
            encoding="utf-8",
        )
        return 0

    payload = {
        "channel": {
            "id": CHANNEL_ID,
            "title": channel_title or "GenAI Practice",
            "url": CHANNEL_URL,
        },
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "videos": videos,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name} with {len(videos)} video(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

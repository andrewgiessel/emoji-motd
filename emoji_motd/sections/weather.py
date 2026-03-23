"""Current weather via wttr.in (no API key needed)."""

from __future__ import annotations

import json
import os
import tempfile
import time
import urllib.request
import urllib.error

from emoji_motd.renderer import center_line

CACHE_FILE = os.path.join(tempfile.gettempdir(), "emoji_motd_weather.json")
CACHE_TTL = 1800  # 30 minutes
TIMEOUT = 1  # seconds


def _read_cache() -> str | None:
    try:
        with open(CACHE_FILE) as f:
            data = json.load(f)
        if time.time() - data.get("ts", 0) < CACHE_TTL:
            return data.get("text")
    except (OSError, json.JSONDecodeError, KeyError):
        pass
    return None


def _write_cache(text: str) -> None:
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({"ts": time.time(), "text": text}, f)
    except OSError:
        pass


def _fetch_weather() -> str | None:
    cached = _read_cache()
    if cached is not None:
        return cached

    try:
        url = "https://wttr.in/?format=%c+%t"
        req = urllib.request.Request(url, headers={"User-Agent": "emoji-motd"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            text = resp.read().decode("utf-8").strip()
        _write_cache(text)
        return text
    except (urllib.error.URLError, OSError, TimeoutError):
        return None


def render(config: dict, context: dict) -> list[str]:
    width = context.get("width", 80)
    should_center = context.get("center", True)

    weather = _fetch_weather()
    if not weather:
        return []

    line = weather
    if should_center:
        line = center_line(line, width)
    return [line]

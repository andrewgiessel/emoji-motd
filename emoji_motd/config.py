"""TOML config loading, defaults, and merging."""

from __future__ import annotations

import os
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]


# Default themes: each maps to a list of section configs.
THEMES: dict[str, list[dict]] = {
    "garden": [
        {"name": "emoji_garden", "rows": 4, "density": "medium", "palette": "seasonal"},
        {"name": "blank", "lines": 1},
        {"name": "oblique"},
    ],
    "night": [
        {"name": "starfield", "rows": 3, "density": "medium"},
        {"name": "blank", "lines": 1},
        {"name": "datetime_info", "format": "friendly"},
    ],
    "synthwave": [
        {"name": "synth_wave", "rows": 5},
        {"name": "blank", "lines": 1},
        {"name": "datetime_info", "format": "friendly"},
    ],
    "minimal": [
        {"name": "datetime_info", "format": "friendly"},
    ],
}

DEFAULT_GENERAL = {
    "theme": "garden",
    "width": "auto",
    "center": True,
}


def config_path() -> Path:
    """Return path to the user's config file."""
    xdg = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    return Path(xdg) / "emoji-motd" / "config.toml"


def load_config(path: Path | None = None) -> dict:
    """Load and merge config from TOML file.

    Returns a dict with 'general' and 'sections' keys.
    """
    cfg: dict = {"general": dict(DEFAULT_GENERAL), "sections": []}

    if path is None:
        path = config_path()

    if path.exists():
        with open(path, "rb") as f:
            user_cfg = tomllib.load(f)
        if "general" in user_cfg:
            cfg["general"].update(user_cfg["general"])
        if "sections" in user_cfg:
            cfg["sections"] = user_cfg["sections"]

    # If no explicit sections, resolve from theme.
    if not cfg["sections"]:
        theme_name = cfg["general"].get("theme", "garden")
        cfg["sections"] = list(THEMES.get(theme_name, THEMES["garden"]))

    return cfg

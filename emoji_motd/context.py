"""Build shared context passed to every section."""

from __future__ import annotations

import os
import shutil
from datetime import datetime


def build_context(config: dict) -> dict:
    """Build the shared context dict for section rendering."""
    now = datetime.now()
    hour = now.hour

    if hour < 12:
        time_of_day = "morning"
    elif hour < 17:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"

    # Terminal width
    general = config.get("general", {})
    width_setting = general.get("width", "auto")
    if width_setting == "auto":
        width = shutil.get_terminal_size((80, 24)).columns
        # Also check $COLUMNS
        env_cols = os.environ.get("COLUMNS")
        if env_cols and env_cols.isdigit():
            width = int(env_cols)
    else:
        width = int(width_setting)

    return {
        "now": now,
        "time_of_day": time_of_day,
        "width": width,
        "center": general.get("center", True),
        "no_color": os.environ.get("NO_COLOR") is not None,
    }

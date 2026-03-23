"""Procedural emoji art grid with weighted palettes.

Inspired by a starfield generator — most cells are empty space, with a
long tail of increasingly rare glyphs. One or two "rich" icons appear
across the entire grid.

Each palette defines three tiers with weights:
  - space: empty cells (" ") — dominates the grid
  - common: subtle texture glyphs — scattered throughout
  - rare: rich, vivid glyphs — only 1-2 per grid
"""

from __future__ import annotations

import random
from datetime import date

from emoji_motd.renderer import center_line


# (common_glyphs, rare_glyphs)
# Space is implicit — controlled by density setting.
PALETTES: dict[str, tuple[list[str], list[str]]] = {
    "spring": (
        ["🌿", "🍃", "🌱", "🌿", "🍃", "🌱"],
        ["🌸", "🌺", "🪷", "🌼", "🌻", "🪻", "🌹", "🌷", "💐", "🦋", "🐝", "🐞"],
    ),
    "summer": (
        ["🌊", "🫧", "💧", "🌀", "〰️", "~"],
        ["🐠", "🦋", "🌺", "🍉", "🦩", "☀️"],
    ),
    "autumn": (
        ["🍂", "🍁", "🍃", "🌾", "🪹", "🌰"],
        ["🦊", "🍄", "🎃", "🐿️", "🦉", "🕯️"],
    ),
    "winter": (
        ["❄️", "✧", "·", "❅", "✦", "∗"],
        ["⛄", "🦌", "🎄", "☕", "🕯️", "🌲"],
    ),
    "ocean": (
        ["🌊", "🫧", "💧", "🌀", "〰️", "·"],
        ["🐚", "🦀", "🐠", "🐙", "🪸", "🐋"],
    ),
    "night": (
        ["·", "✦", "✧", "⋆", "∗", "˚"],
        ["🌙", "🪐", "🦉", "✨", "🌠", "💫"],
    ),
    "desert": (
        ["🪨", "·", "🌾", "∗", "☼", "⋯"],
        ["🌵", "🦎", "🐪", "🦂", "🦅", "🏺"],
    ),
    "forest": (
        ["🌲", "🌿", "🍃", "☘️", "🌱", "🍀"],
        ["🦌", "🦊", "🐿️", "🍄", "🦉", "🐻"],
    ),
    "tropical": (
        ["🌴", "🌿", "🍃", "🌱", "☘️", "🫧"],
        ["🦜", "🌺", "🍍", "🦩", "🌈", "🦋"],
    ),
}

# Approximate equinox/solstice boundaries (month, day) for Northern Hemisphere
_SEASON_BOUNDARIES = [
    ((3, 20), "spring"),
    ((6, 21), "summer"),
    ((9, 22), "autumn"),
    ((12, 21), "winter"),
]


def _get_seasonal_palette() -> str:
    today = date.today()
    md = (today.month, today.day)
    if md >= (12, 21) or md < (3, 20):
        return "winter"
    if md >= (9, 22):
        return "autumn"
    if md >= (6, 21):
        return "summer"
    return "spring"


def _pick_cell(common: list[str], weights: list[float]) -> str:
    """Weighted random pick: space or one of the common glyphs."""
    # weights[0] = space probability, rest split across common glyphs
    r = random.random()
    if r < weights[0]:
        return " "
    # Distribute remaining probability evenly across common glyphs
    return random.choice(common)


def render(config: dict, context: dict) -> list[str]:
    rows = config.get("rows", 4)
    density = config.get("density", "medium")
    palette_name = config.get("palette", "seasonal")
    width = context.get("width", 80)
    should_center = context.get("center", True)

    if palette_name == "seasonal":
        palette_name = _get_seasonal_palette()
    elif palette_name == "random":
        palette_name = random.choice(list(PALETTES.keys()))

    common, rare = PALETTES.get(palette_name, PALETTES["spring"])

    # Density controls how much empty space
    # Like the Racket code: sparse ~88% space, medium ~80%, dense ~65%
    space_weight = {"sparse": 0.88, "medium": 0.80, "dense": 0.65}.get(density, 0.80)

    # Use ~60% of terminal width for the grid
    cols = min(int(width * 0.6), 50)
    total_cells = rows * cols

    # Place 2-3 rare glyphs across the entire grid
    num_rare = random.randint(2, 3)
    rare_positions = set(random.sample(range(total_cells), min(num_rare, total_cells)))

    lines = []
    for row_idx in range(rows):
        cells = []
        for col_idx in range(cols):
            pos = row_idx * cols + col_idx
            if pos in rare_positions:
                cells.append(random.choice(rare))
            else:
                if random.random() < space_weight:
                    cells.append(" ")
                else:
                    cells.append(random.choice(common))
        row_str = " ".join(cells)
        if should_center:
            row_str = center_line(row_str, width)
        lines.append(row_str)

    return lines

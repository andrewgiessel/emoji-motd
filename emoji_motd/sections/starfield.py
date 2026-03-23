"""Unicode starfield with varying densities."""

from __future__ import annotations

import random

STAR_CHARS = ["·", "✦", "★", "✧", "✶", "⋆", "∗"]
BRIGHT_STARS = ["★", "✦"]
DIM_STARS = ["·", "✧", "⋆"]


def render(config: dict, context: dict) -> list[str]:
    rows = config.get("rows", 3)
    density = config.get("density", "medium")
    width = context.get("width", 80)
    no_color = context.get("no_color", False)

    density_map = {"sparse": 0.06, "medium": 0.10, "dense": 0.16}
    fill_pct = density_map.get(density, 0.10)

    lines = []
    for _ in range(rows):
        row = [" "] * width
        num_stars = int(width * fill_pct)
        positions = random.sample(range(width), min(num_stars, width))
        for pos in positions:
            char = random.choice(STAR_CHARS)
            if not no_color and char in BRIGHT_STARS:
                row[pos] = f"\033[1m{char}\033[0m"
            elif not no_color and char in DIM_STARS:
                row[pos] = f"\033[2m{char}\033[0m"
            else:
                row[pos] = char
        lines.append("".join(row))

    return lines

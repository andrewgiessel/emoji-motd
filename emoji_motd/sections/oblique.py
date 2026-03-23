"""Brian Eno's Oblique Strategies — pick a random card."""

from __future__ import annotations

import random

from emoji_motd.renderer import center_line, ITALIC, RESET, DIM
from emoji_motd.sections.oblique_strategies import CARDS


def render(config: dict, context: dict) -> list[str]:
    edition = config.get("edition", "all")
    width = context.get("width", 80)
    should_center = context.get("center", True)
    no_color = context.get("no_color", False)

    if edition == "all":
        pool = CARDS
    else:
        year = int(edition)
        pool = [c for c in CARDS if year in c["editions"]]
        if not pool:
            pool = CARDS

    card = random.choice(pool)
    text = f'"{card["text"]}"'

    if not no_color:
        text = f"{ITALIC}{DIM}{text}{RESET}"

    align = config.get("align", "center" if should_center else "left")
    indent = config.get("indent", 0)

    if align == "center":
        text = center_line(text, width)
    else:
        text = " " * indent + text

    return [text]

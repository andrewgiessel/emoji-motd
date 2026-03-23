"""ANSI color helpers and unicode-aware padding/centering."""

from __future__ import annotations

import re
import unicodedata


# --- ANSI escape helpers ---

def sgr(*codes: int) -> str:
    """Build an SGR escape sequence."""
    return f"\033[{';'.join(str(c) for c in codes)}m"


RESET = sgr(0)
BOLD = sgr(1)
DIM = sgr(2)
ITALIC = sgr(3)
UNDERLINE = sgr(4)


def fg256(n: int) -> str:
    """Foreground color from the 256-color palette."""
    return f"\033[38;5;{n}m"


def bg256(n: int) -> str:
    """Background color from the 256-color palette."""
    return f"\033[48;5;{n}m"


def fg_rgb(r: int, g: int, b: int) -> str:
    """Foreground truecolor."""
    return f"\033[38;2;{r};{g};{b}m"


def bg_rgb(r: int, g: int, b: int) -> str:
    """Background truecolor."""
    return f"\033[48;2;{r};{g};{b}m"


# --- Unicode display width ---

_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from text."""
    return _ANSI_RE.sub("", text)


def display_width(text: str) -> int:
    """Calculate the display width of text, accounting for wide characters and ANSI escapes."""
    text = strip_ansi(text)
    width = 0
    for ch in text:
        cat = unicodedata.east_asian_width(ch)
        if cat in ("W", "F"):
            width += 2
        else:
            width += 1
    return width


def center_line(text: str, width: int) -> str:
    """Center a line within the given width, respecting unicode display widths."""
    text_width = display_width(text)
    if text_width >= width:
        return text
    padding = (width - text_width) // 2
    return " " * padding + text


def pad_right(text: str, width: int) -> str:
    """Pad text on the right to fill the given width."""
    text_width = display_width(text)
    if text_width >= width:
        return text
    return text + " " * (width - text_width)

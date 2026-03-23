"""Section discovery, registry, and composition."""

from __future__ import annotations

import importlib
import logging
from typing import Callable

log = logging.getLogger("emoji_motd")

# Section render function type
RenderFunc = Callable[[dict, dict], list[str]]


def load_section(name: str) -> RenderFunc | None:
    """Dynamically import a section module and return its render function."""
    module_name = f"emoji_motd.sections.{name}"
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        log.debug("Section %r not found", name)
        return None

    render = getattr(module, "render", None)
    if render is None:
        log.debug("Section %r has no render() function", name)
        return None

    return render


def list_sections() -> list[str]:
    """Return names of all available built-in sections."""
    from emoji_motd.sections import __path__ as sections_path
    from pathlib import Path

    names = []
    for p in sections_path:
        for f in sorted(Path(p).glob("*.py")):
            if f.name.startswith("_"):
                continue
            # Skip data-only modules (no render function)
            if f.stem == "oblique_strategies":
                continue
            names.append(f.stem)
    return names


def compose(config: dict, context: dict) -> str:
    """Load and render all configured sections, return final output string."""
    lines: list[str] = []

    for section_cfg in config.get("sections", []):
        name = section_cfg.get("name", "")
        render = load_section(name)
        if render is None:
            continue
        try:
            section_lines = render(section_cfg, context)
        except Exception:
            log.debug("Section %r failed", name, exc_info=True)
            continue
        lines.extend(section_lines)

    return "\n".join(lines)

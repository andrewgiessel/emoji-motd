"""Configurable blank line spacer."""

from __future__ import annotations


def render(config: dict, context: dict) -> list[str]:
    lines = config.get("lines", 1)
    return [""] * lines

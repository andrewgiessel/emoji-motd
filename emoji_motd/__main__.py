"""Entry point for `python -m emoji_motd` and the `emoji-motd` command."""

from __future__ import annotations

import argparse
import sys

from emoji_motd.config import THEMES, load_config
from emoji_motd.context import build_context
from emoji_motd.core import compose, list_sections


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="emoji-motd",
        description="Emoji Message-of-the-Day for your terminal",
    )
    parser.add_argument(
        "--theme",
        choices=list(THEMES.keys()),
        help="Use a predefined theme",
    )
    parser.add_argument(
        "--list-sections",
        action="store_true",
        help="List available sections and exit",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color output",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to config TOML file",
    )

    args = parser.parse_args(argv)

    if args.list_sections:
        for name in list_sections():
            print(f"  {name}")
        return

    # Load config
    from pathlib import Path

    config_path = Path(args.config) if args.config else None
    config = load_config(config_path)

    # Override theme from CLI
    if args.theme:
        config["general"]["theme"] = args.theme
        config["sections"] = list(THEMES[args.theme])

    # Build context
    context = build_context(config)
    if args.no_color:
        context["no_color"] = True

    # Render and print
    output = compose(config, context)
    if output.strip():
        print(output)


if __name__ == "__main__":
    main()

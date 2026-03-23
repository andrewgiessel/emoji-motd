# emoji-motd

A pluggable, terminal-native Python library for generating emoji-rich Message-of-the-Day banners. Inspired by [spaceship-prompt](https://github.com/spaceship-prompt/spaceship-prompt)'s modular section architecture — but instead of a prompt, it renders a visual greeting every time you open a shell.

## Vision

When you open a terminal, you see something like:

```
  🌿 🌸 🐝 🌻 🍄 🌿 🦋 🌺
  🌱 🪷 🐞 🌼 🌿 🍃 🌸 🪻

  Monday, March 23 — 68°F partly cloudy
  "Honor thy error as a hidden intention"  — Oblique Strategies
```

Or on another day, a starfield:

```
  ·  ✦     ·    ★   ·      ✧
     ·   ✧    ·    ·  ✦  ·
  ✧     ·  ★    ·     ·   ✦

  Good morning, Andrew.
```

Each visual element is a **section** — a small, self-contained module that returns lines of styled text. The framework composes sections together.

## Architecture

### Spaceship-inspired section protocol

Every section is a Python module in `emoji_motd/sections/` that exposes:

```python
def render(config: dict, context: dict) -> list[str]:
    """Return lines of text for this section.

    Args:
        config: Per-section config from the user's TOML file.
        context: Shared context (terminal width, time of day, etc.)

    Returns:
        List of strings (one per line). Empty list = section is hidden.
    """
```

That's it. The entire contract is one function.

### Core modules

```
emoji_motd/
├── __init__.py           # version, public API
├── __main__.py           # `python -m emoji_motd` entry point
├── core.py               # section discovery, registry, composition
├── renderer.py           # ANSI color helpers, unicode-aware padding
├── config.py             # TOML config loading, defaults, merging
├── context.py            # build shared context (term width, time, etc.)
└── sections/
    ├── __init__.py
    ├── emoji_garden.py   # procedural emoji art grid
    ├── starfield.py      # unicode starfield with varying densities
    ├── synth_wave.py     # block-character waveform art
    ├── datetime_info.py  # date, time, greeting based on time of day
    ├── weather.py        # current weather via wttr.in (no API key needed)
    ├── oblique.py        # Brian Eno's Oblique Strategies
    └── blank.py          # configurable blank line spacer
```

### Config (TOML)

```toml
# ~/.config/emoji-motd/config.toml

[general]
theme = "garden"   # predefined combos, or use [sections] for custom
width = "auto"     # "auto" = detect terminal width
center = true

# Sections render top-to-bottom in this order.
# Comment out or remove a section to disable it.
[[sections]]
name = "emoji_garden"
rows = 2
density = "medium"   # sparse, medium, dense
palette = "spring"   # spring, ocean, night, desert, random

[[sections]]
name = "blank"
lines = 1

[[sections]]
name = "datetime_info"
format = "friendly"  # friendly, iso, minimal

[[sections]]
name = "oblique"
edition = "all"      # all, original, 1975, 1978, 1979, 1996, 2001
```

### Themes

Themes are just predefined section+config combos:

- **garden** — emoji_garden + datetime_info + oblique
- **night** — starfield + datetime_info
- **synthwave** — synth_wave + datetime_info
- **minimal** — datetime_info only

Users can override any theme setting or ignore themes entirely with explicit `[[sections]]`.

## Implementation priorities

Build these in order:

1. **Core framework** — `core.py`, `config.py`, `context.py`, `__main__.py`. Get the section-loading and composition loop working first. Start with a hardcoded section list, then add TOML config.
2. **Renderer** — ANSI 256-color and truecolor helpers, unicode-width-aware centering/padding. Keep it dependency-free (no `rich` or `colorama`) — just raw ANSI escape codes. The library should have zero required dependencies.
3. **emoji_garden section** — The signature section. Procedurally generates an emoji grid with configurable palettes. Palettes are just lists of emoji grouped by vibe (spring: 🌿🌸🐝🌻🍄🦋🌺🪷🐞🌼🍃🪻, ocean: 🌊🐚🦀🐠🪸🦈🐙🐋🫧, etc.).
4. **starfield section** — Unicode dot/star characters at random positions. Vary density and character set.
5. **datetime_info section** — Time-of-day greeting + formatted date. Simple but it anchors every theme.
6. **oblique section** — Brian Eno & Peter Schmidt's Oblique Strategies. Ship the full card set as a bundled Python data file (`oblique_strategies.py` with a `CARDS` list). Each card is a short string. The section picks one at random and renders it in italics (via ANSI). Optionally filter by edition (the deck was published in several editions: 1975, 1978, 1979, 1996, 2001 — each added/removed/revised cards). Default: draw from all editions combined.
7. **synth_wave section** — Block characters (▁▂▃▄▅▆▇█) forming a sine wave pattern. Color gradient across the wave.
8. **weather section** — Fetch from `wttr.in` (just `curl wttr.in/?format=...`). Graceful timeout/failure — if the network is slow, skip silently.
9. **blank section** — Trivial but useful for layout control.
10. **CLI polish** — `emoji-motd` entry point via pyproject.toml, `--theme` flag, `--list-sections`, `--no-color`.

## Design principles

- **Zero required dependencies.** stdlib only for core + all bundled sections. The weather section may use `urllib` from stdlib.
- **Fast startup.** This runs on every shell open. Target < 100ms for non-network sections. Lazy-import anything heavy. Weather section should have an aggressive timeout (1s) and cache results for ~30min in `/tmp`.
- **Graceful degradation.** If a section fails, log a debug message and skip it — never crash the MOTD. If the terminal doesn't support color, fall back to plain text.
- **Terminal-width-aware.** Detect width and center/wrap accordingly. Respect `$COLUMNS`.
- **Fun to hack on.** Adding a new section should be: create a file, write one function, done. No registration boilerplate.

## Integration

Add to `~/.zshrc` (works alongside spaceship prompt):

```zsh
# Show MOTD on new shell (not on every prompt)
python3 -m emoji_motd
```

Or with a specific theme:

```zsh
python3 -m emoji_motd --theme night
```

## Tech details

- Python 3.10+ (match statements are fine, f-strings, type hints)
- Use `pyproject.toml` for packaging (no setup.py)
- `[project.scripts]` entry point: `emoji-motd = "emoji_motd.__main__:main"`
- Testing with pytest. Each section should be independently testable — give it a config and context, assert it returns a list of strings of reasonable width.
- No classes unless they genuinely help. Functions and modules are the primary unit of organization, matching the spaceship style.

## Non-goals (for now)

- No web/browser rendering. This is terminal-only.
- No interactive elements. It prints and exits.
- No daemon/resident process. Stateless on each invocation (except temp cache for weather).
- No prompt integration. This is MOTD, not a prompt theme. It runs once when the shell starts, not on every command.

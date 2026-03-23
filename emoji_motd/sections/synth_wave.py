"""Block-character waveform art with color gradient."""

from __future__ import annotations

import math

from emoji_motd.renderer import center_line, fg_rgb, RESET

BLOCKS = " ▁▂▃▄▅▆▇█"


def render(config: dict, context: dict) -> list[str]:
    rows = config.get("rows", 5)
    width = context.get("width", 80)
    should_center = context.get("center", True)
    no_color = context.get("no_color", False)

    # Use ~60% of terminal width for the wave
    wave_width = min(int(width * 0.6), 60)

    # Generate sine wave heights (0 to rows-1)
    heights = []
    for i in range(wave_width):
        t = i / wave_width * 2 * math.pi * 2  # two full cycles
        val = (math.sin(t) + 1) / 2  # normalize to 0..1
        heights.append(val)

    # Build the grid row by row (top to bottom)
    lines = []
    for row in range(rows):
        threshold = (rows - 1 - row) / rows  # top rows = high threshold
        chars = []
        for col, h in enumerate(heights):
            if h >= threshold + 1 / rows:
                block = BLOCKS[8]  # full block
            elif h >= threshold:
                # partial block
                frac = (h - threshold) * rows
                idx = int(frac * 8)
                block = BLOCKS[min(idx, 8)]
            else:
                block = " "

            if not no_color and block != " ":
                # Gradient: magenta -> cyan across the wave
                r = int(200 * (1 - col / wave_width))
                g = int(50 + 150 * (col / wave_width))
                b = int(200 + 55 * (col / wave_width))
                chars.append(f"{fg_rgb(r, g, b)}{block}{RESET}")
            else:
                chars.append(block)

        line = "".join(chars)
        if should_center:
            line = center_line(line, width)
        lines.append(line)

    return lines

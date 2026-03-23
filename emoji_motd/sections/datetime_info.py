"""Date, time, and greeting based on time of day."""

from __future__ import annotations

from emoji_motd.renderer import center_line


def render(config: dict, context: dict) -> list[str]:
    fmt = config.get("format", "friendly")
    now = context["now"]
    time_of_day = context["time_of_day"]
    width = context.get("width", 80)
    should_center = context.get("center", True)

    if fmt == "iso":
        date_str = now.strftime("%Y-%m-%d %H:%M")
    elif fmt == "minimal":
        date_str = now.strftime("%a %b %d")
    else:
        # friendly
        day_name = now.strftime("%A")
        month_day = now.strftime("%B %-d")
        date_str = f"{day_name}, {month_day}"

    greeting = f"Good {time_of_day}."

    line = f"{date_str}  —  {greeting}"
    if should_center:
        line = center_line(line, width)

    return [line]

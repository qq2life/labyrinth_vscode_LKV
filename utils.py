"""Утилиты и вспомогательные функции."""
from __future__ import annotations

from textwrap import fill


def wrap(text: str, width: int = 88) -> str:
    return fill(text, width=width)


def normalize_tokens(s: str) -> list[str]:
    return s.strip().lower().split()


def render_room(room: dict) -> str:
    parts: list[str] = [room["desc"]]
    items = room.get("items", [])
    if items:
        parts.append("Здесь лежит: " + ", ".join(items))
    puzzle = room.get("puzzle")
    if puzzle:
        parts.append("На колонне загадка. Попробуйте: solve <загадка> <ответ>")
    trap = room.get("trap")
    if trap:
        parts.append(f"Похоже, тут ловушка: {trap['note']}")
    return wrap("\n".join(parts))


def ensure_direction(token: str) -> str | None:
    aliases = {
        "с": "north",
        "в": "east",
        "ю": "south",
        "з": "west",
        "север": "north",
        "восток": "east",
        "юг": "south",
        "запад": "west",
        "north": "north",
        "east": "east",
        "south": "south",
        "west": "west",
    }
    return aliases.get(token)
"""Игровые действия игрока."""
from __future__ import annotations

import random
from typing import Any

from constants import ROOMS, VICTORY_TEXT
from utils import ensure_direction, render_room, wrap


class GameState:
    def __init__(self) -> None:
        self.location: str = "Вход"
        self.inventory: set[str] = set()
        self.solved: set[str] = set()
        self.game_over: bool = False
        self.victory: bool = False

    # --- базовые действия ---
    def look(self) -> str:
        return render_room(ROOMS[self.location])

    def inventory_cmd(self) -> str:
        return (
            "Инвентарь пуст."
            if not self.inventory
            else "У вас: " + ", ".join(sorted(self.inventory))
        )

    def go(self, token: str | None) -> str:
        if not token:
            return "Куда идти? Используйте: go <направление>."
        direction = ensure_direction(token)
        if not direction:
            return "Не понимаю направление. Попробуйте север/юг/восток/запад."
        exits = ROOMS[self.location]["exits"]
        if direction not in exits:
            return "Туда пути нет."
        # шанс случайного события при перемещении
        self._maybe_event_before_move()
        self.location = exits[direction]
        self._maybe_trap()
        return self.look()

    def take(self, item: str | None) -> str:
        if not item:
            return "Что взять?"
        room = ROOMS[self.location]
        items = room.get("items", [])
        if item not in items:
            return "Здесь такого нет."
        self.inventory.add(item)
        items.remove(item)
        return f"Вы взяли: {item}."

    def use(self, item: str | None, target: str | None) -> str:
        if not item:
            return "Использовать что?"
        if item not in self.inventory:
            return "У вас нет такого предмета."

        # Открытие сундука — условие победы
        if self.location == "Сокровищница" and item == "золотой ключ":
            room = ROOMS[self.location]
            if room.get("locked", False):
                room["locked"] = False
                self.victory = True
                self.game_over = True
                return VICTORY_TEXT
            return "Сундук уже открыт."

        return "Пока это не помогает."

    def solve(self, puzzle_id: str | None, *answer: str) -> str:
        room = ROOMS[self.location]
        puzzle = room.get("puzzle")
        if not puzzle:
            return "Здесь нет загадок."
        if not puzzle_id or puzzle_id != puzzle["id"]:
            return "Уточните: solve <загадка> <ответ>."
        if not answer:
            return "Нужен ответ на загадку."
        ans = " ".join(answer)
        if ans.lower().strip().rstrip("!?.") in puzzle["answer"]:
            if puzzle["id"] in self.solved:
                return "Эта загадка уже решена."
            self.solved.add(puzzle["id"])
            reward = puzzle.get("reward")
            if reward:
                self.inventory.add(reward)
            return wrap(
                "Колонна дрогнула, послышался щелчок. Вы получили предмет: " + reward
            )
        return "Ответ неверный."

    def quit(self) -> str:
        self.game_over = True
        return "Вы решили закончить приключение. "

    # --- служебные механики ---
    def _maybe_trap(self) -> None:
        room = ROOMS[self.location]
        trap = room.get("trap")
        if not trap:
            return
        chance = 0.4
        if random.random() < chance:
            kind = trap["kind"]
            if kind == "дротики":
                if "амулет" in self.inventory:
                    # амулет спасает, но ломается
                    self.inventory.discard("амулет")
                else:
                    # откат в прошлую комнату, если есть
                    # найдём вход, ведущий обратно
                    for d, r in ROOMS.items():
                        if self.location in r.get("exits", {}).values():
                            self.location = d
                            break
            elif kind == "яма":
                if "щит" in self.inventory:
                    # щит спасает и остаётся
                    return
                else:
                    # потеря случайного предмета (если он есть)
                    if self.inventory:
                        self.inventory.pop()

    def _maybe_event_before_move(self) -> None:
        # лёгкое случайное событие
        if random.random() < 0.2 and "факел" not in self.inventory:
            # без факела темно: следующая комната описана туманно
            pass  # эффект описан текстом в look(), упрощаем


def help_text() -> str:
    lines = ["Доступные команды:"]
    lines.extend(" - " + c for c in (
        "go <направление>",
        "look",
        "inventory",
        "take <предмет>",
        "use <предмет> [на_объект]",
        "solve <загадка> <ответ>",
        "quit",
        "help",
    ))
    return "\n".join(lines)
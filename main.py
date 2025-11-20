"""Точка входа. Игровой цикл и парсинг команд."""
from __future__ import annotations

from constants import COMMANDS, GAME_OVER_TEXT, INTRO_TEXT
from player_actions import GameState, help_text
from utils import normalize_tokens


def main() -> None:
    state = GameState()
    print(INTRO_TEXT)
    print(state.look())

    while not state.game_over:
        try:
            raw = input("\n> ")
        except (EOFError, KeyboardInterrupt):
            print("\nДо встречи в лабиринте!")
            break

        tokens = normalize_tokens(raw)
        if not tokens:
            continue
        cmd, *args = tokens

        if cmd == "look":
            print(state.look())
        elif cmd in {"inv", "inventory"}:
            print(state.inventory_cmd())
        elif cmd in {"go", "идти"}:
            arg = args[0] if args else None
            print(state.go(arg))
        elif cmd == "take":
            print(state.take(args[0] if args else None))
        elif cmd == "use":
            item = args[0] if args else None
            target = args[1] if len(args) > 1 else None
            print(state.use(item, target))
        elif cmd == "solve":
            puzzle = args[0] if args else None
            answer = args[1:] if len(args) > 1 else []
            print(state.solve(puzzle, *answer))
        elif cmd in {"help", "?"}:
            print(help_text())
        elif cmd in {"quit", "exit"}:
            print(state.quit())
        else:
            print(
                "Неизвестная команда. Попробуйте 'help'. Доступно: " + ", ".join(COMMANDS)
            )

    print(GAME_OVER_TEXT)


if __name__ == "__main__":
    main()
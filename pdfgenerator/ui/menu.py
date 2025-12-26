"""Модуль для работы с меню."""

import sys
from typing import Any, Callable, Optional


class Menu:
    """Класс для работы с консольным меню."""

    @staticmethod
    def print_menu(
        title: str, items: list[Any], item_formatter: Optional[Callable] = None
    ) -> None:
        """Вывести красивое меню с нумерацией."""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        for i, item in enumerate(items, 1):
            display = item_formatter(item) if item_formatter else str(item)
            print(f"  {i}. {display}")
        print(f"{'='*60}\n")

    @staticmethod
    def get_user_choice(
        items: list[Any], prompt: str = "Выберите вариант"
    ) -> Optional[Any]:
        """Получить выбор пользователя из списка."""
        if not items:
            return None

        while True:
            try:
                choice = input(f"{prompt} (1-{len(items)}): ").strip()
                index = int(choice) - 1
                if 0 <= index < len(items):
                    return items[index]
                else:
                    print(f"Пожалуйста, введите число от 1 до {len(items)}")
            except ValueError:
                print("Пожалуйста, введите корректное число")
            except KeyboardInterrupt:
                print("\n\nОперация отменена.")
                sys.exit(0)

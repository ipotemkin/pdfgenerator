"""Рендерер для HTML шаблонов."""

import re
from typing import Any


class TemplateRenderer:
    """Класс для рендеринга HTML шаблонов с данными."""

    def render(self, template: str, data: dict[str, Any]) -> str:
        """Подставить данные в HTML шаблон."""
        # Обрабатываем items, если они есть
        processed_data = data.copy()

        # Если есть поле items (список словарей), конвертируем в HTML
        if "items" in processed_data and isinstance(
            processed_data["items"], list
        ):
            items_html = ""
            for item in processed_data["items"]:
                name = item.get("name", "")
                quantity = item.get("quantity", 0)
                price = item.get("price", 0.0)
                item_total = quantity * price
                items_html += (
                    f"<tr><td>{name}</td><td>{quantity}</td>"
                    f"<td>{price:.2f} ₽</td><td>{item_total:.2f} ₽</td></tr>\n"
                )
            processed_data["items_html"] = items_html
        # Если данные в плоском формате (CSV с item_name, quantity, price)
        elif "item_name" in processed_data:
            name = processed_data.get("item_name", "")
            quantity = float(processed_data.get("quantity", 0))
            price = float(processed_data.get("price", 0.0))
            item_total = quantity * price
            processed_data["items_html"] = (
                f"<tr><td>{name}</td><td>{int(quantity)}</td><td>{price:.2f} ₽"
                f"</td><td>{item_total:.2f} ₽</td></tr>\n"
            )

        # Если items_html не был создан, создаем пустую строку
        if "items_html" not in processed_data:
            processed_data["items_html"] = (
                "<tr><td colspan='4'>Нет данных</td></tr>"
            )

        # Используем безопасную замену через регулярные выражения
        # Это позволяет избежать проблем с фигурными скобками в CSS
        result = template

        # Находим все плейсхолдеры вида {key} или {key:format} в шаблоне
        # Игнорируем экранированные {{ и }}
        placeholder_pattern = re.compile(r"(?<!\{)\{([^}]+)\}(?!\})")

        def replace_placeholder(match):
            placeholder = match.group(1)
            # Разделяем ключ и формат (если есть)
            if ":" in placeholder:
                key, format_spec = placeholder.split(":", 1)
            else:
                key = placeholder
                format_spec = None

            if key in processed_data:
                value = processed_data[key]
                # Применяем форматирование, если указано
                if format_spec:
                    try:
                        # Для чисел применяем форматирование
                        if isinstance(value, (int, float)):
                            formatted_value = format(value, format_spec)
                        else:
                            formatted_value = format(str(value), format_spec)
                    except (ValueError, TypeError):
                        formatted_value = str(value)
                else:
                    # Без форматирования
                    if isinstance(value, float):
                        formatted_value = f"{value:.2f}"
                    else:
                        formatted_value = str(value)
                return formatted_value
            else:
                # Если ключ не найден, оставляем плейсхолдер как есть
                return match.group(0)

        result = placeholder_pattern.sub(replace_placeholder, result)
        return result

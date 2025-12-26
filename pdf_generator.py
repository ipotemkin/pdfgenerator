#!/usr/bin/env python3
"""
CLI-утилита для генерации PDF документов из данных и HTML-шаблонов.
"""

import csv
import json
import os
import platform
import re
import sys
from pathlib import Path
from typing import Any, Optional, cast

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from weasyprint import CSS, HTML  # type: ignore
    from weasyprint.text.fonts import FontConfiguration  # type: ignore
except ImportError:
    print("Ошибка: библиотека WeasyPrint не установлена.")
    print("Установите её командой: pip install weasyprint")
    sys.exit(1)


class PDFGenerator:
    """Класс для генерации PDF документов."""

    def __init__(
        self,
        data_dir: str = "data",
        templates_dir: str = "templates",
        output_dir: str = "output",
    ):
        self.data_dir = Path(data_dir)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)

        # Создаем директории, если их нет
        self.data_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

        # Настройка шрифта для кириллицы
        self.font_config = FontConfiguration()
        self.css = CSS(
            string="""
            @page {
                size: A4;
                margin: 2cm;
            }
            body {
                font-family: "DejaVu Sans", "Roboto", Arial, sans-serif;
                font-size: 12pt;
            }
        """,
            font_config=self.font_config,
        )

    def get_data_files(self) -> list[Path]:
        """Получить список всех CSV, JSON и XLSX файлов из директории data."""
        data_files: list[Path] = []
        if self.data_dir.exists():
            for ext in ["*.csv", "*.json", "*.xlsx"]:
                data_files.extend(self.data_dir.glob(ext))
        return sorted(data_files)

    def get_template_files(self) -> list[Path]:
        """Получить список всех HTML шаблонов из директории templates."""
        templates = []
        if self.templates_dir.exists():
            templates = list(self.templates_dir.glob("*.html"))
        return sorted(templates)

    def load_data_file(self, file_path: Path) -> list[dict[str, Any]]:
        """Загрузить данные из CSV, JSON или XLSX файла."""
        if file_path.suffix.lower() == ".json":
            with open(file_path, encoding="utf-8") as f:
                data: Any = json.load(f)
                # Если это список, возвращаем как есть
                if isinstance(data, list):
                    return cast(list[dict[str, Any]], data)
                # Если это словарь, оборачиваем в список
                elif isinstance(data, dict):
                    return [cast(dict[str, Any], data)]
                else:
                    return []

        elif file_path.suffix.lower() == ".csv":
            if PANDAS_AVAILABLE:
                df = pd.read_csv(file_path, encoding="utf-8")
                records = df.to_dict("records")
                return cast(list[dict[str, Any]], records)
            else:
                # Используем стандартную библиотеку csv
                csv_data: list[dict[str, Any]] = []
                with open(file_path, encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        csv_data.append(dict(row))
                return csv_data

        elif file_path.suffix.lower() == ".xlsx":
            if PANDAS_AVAILABLE:
                # Читаем первый лист Excel файла
                df = pd.read_excel(file_path, engine="openpyxl")
                records = df.to_dict("records")
                return cast(list[dict[str, Any]], records)
            else:
                print(
                    "Ошибка: для чтения XLSX файлов требуется pandas. "
                    "Установите: pip install pandas openpyxl"
                )
                return []

        return []

    def load_template(self, template_path: Path) -> str:
        """Загрузить HTML шаблон."""
        with open(template_path, encoding="utf-8") as f:
            return f.read()

    def render_template(self, template: str, data: dict[str, Any]) -> str:
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

    def generate_pdf(self, html_content: str, output_path: Path) -> None:
        """Сгенерировать PDF из HTML контента."""
        HTML(string=html_content).write_pdf(
            output_path, stylesheets=[self.css], font_config=self.font_config
        )

    def open_pdf(self, pdf_path: Path) -> None:
        """Открыть PDF в системной программе."""
        system = platform.system()
        pdf_path_str = str(pdf_path.absolute())

        if system == "Darwin":  # macOS
            os.system(f'open "{pdf_path_str}"')
        elif system == "Windows":
            os.system(f'start "" "{pdf_path_str}"')
        elif system == "Linux":
            os.system(f'xdg-open "{pdf_path_str}"')
        else:
            print(f"PDF сохранен: {pdf_path_str}")


def print_menu(title: str, items: list[Any], item_formatter=None) -> None:
    """Вывести красивое меню с нумерацией."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    for i, item in enumerate(items, 1):
        display = item_formatter(item) if item_formatter else str(item)
        print(f"  {i}. {display}")
    print(f"{'='*60}\n")


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


def main():
    """Основная функция программы."""
    generator = PDFGenerator()

    print("\n" + "=" * 60)
    print("  ГЕНЕРАТОР PDF ДОКУМЕНТОВ")
    print("=" * 60)

    # Получаем списки файлов
    data_files = generator.get_data_files()
    template_files = generator.get_template_files()

    # Проверяем наличие файлов
    if not data_files:
        print(
            "\nОшибка: не найдено ни одного файла данных "
            "(CSV/JSON/XLSX) в директории 'data'"
        )
        print("Пожалуйста, добавьте файлы данных в директорию 'data'")
        return

    if not template_files:
        print(
            "\nОшибка: не найдено ни одного HTML шаблона "
            "в директории 'templates'"
        )
        print("Пожалуйста, добавьте HTML шаблоны в директорию 'templates'")
        return

    # Выводим меню выбора файла данных
    print_menu(
        "Доступные файлы с данными",
        data_files,
        item_formatter=lambda f: f"{f.name} ({f.suffix.upper()})",
    )

    selected_data_file = get_user_choice(data_files, "Выберите файл с данными")
    if not selected_data_file:
        return

    # Выводим меню выбора шаблона
    print_menu(
        "Доступные HTML шаблоны",
        template_files,
        item_formatter=lambda f: f.name,
    )

    selected_template = get_user_choice(template_files, "Выберите HTML шаблон")
    if not selected_template:
        return

    # Загружаем данные и шаблон
    print(f"\nЗагрузка данных из {selected_data_file.name}...")
    data = generator.load_data_file(selected_data_file)

    if not data:
        print("Ошибка: файл данных пуст или не содержит данных")
        return

    print(f"Загрузка шаблона {selected_template.name}...")
    template = generator.load_template(selected_template)

    # Извлекаем invoice_id из данных
    # Ищем поле invoice_id, invoice_id, invoice, id и т.д.
    invoice_key = None
    for key in ["invoice_id", "invoiceId", "invoice", "id", "ID"]:
        if key in data[0]:
            invoice_key = key
            break

    if not invoice_key:
        print(
            "Предупреждение: не найдено поле с invoice ID. "
            "Используется порядковый номер."
        )
        invoices = [(i + 1, f"Запись #{i+1}") for i in range(len(data))]
    else:
        invoices = [
            (i, str(record.get(invoice_key, f"Запись #{i+1}")))
            for i, record in enumerate(data)
        ]

    # Выводим меню выбора invoice
    print_menu(
        "Доступные счета (invoices)",
        invoices,
        item_formatter=lambda item: f"ID: {item[1]}",
    )

    selected_invoice_index = get_user_choice(invoices, "Выберите invoice ID")

    if not selected_invoice_index:
        return

    invoice_index = selected_invoice_index[0]
    invoice_data = data[invoice_index]

    # Генерируем PDF
    print(f"\nГенерация PDF для invoice ID: {selected_invoice_index[1]}...")

    try:
        html_content = generator.render_template(template, invoice_data)
        invoice_id = str(invoice_data.get(invoice_key, invoice_index + 1))
        safe_invoice_id = "".join(
            c for c in invoice_id if c.isalnum() or c in ("-", "_")
        )
        output_filename = f"invoice_{safe_invoice_id}.pdf"
        output_path = generator.output_dir / output_filename

        generator.generate_pdf(html_content, output_path)
        print(f"✓ PDF успешно создан: {output_path}")

        # Открываем PDF
        print("Открытие PDF...")
        generator.open_pdf(output_path)

    except Exception as e:
        print(f"Ошибка при генерации PDF: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

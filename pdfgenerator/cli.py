#!/usr/bin/env python3
"""Точка входа в приложение PDF Generator."""

from typing import Any, Optional, TYPE_CHECKING

from pdfgenerator.core import FileManager
from pdfgenerator.templates import TemplateRenderer
from pdfgenerator.ui import Menu

if TYPE_CHECKING:
    from pdfgenerator.core.generator import PDFGenerator


def find_invoice_key(data: list[dict[str, Any]]) -> Optional[str]:
    """Найти ключ для invoice ID в данных."""
    if not data:
        return None

    for key in ["invoice_id", "invoiceId", "invoice", "id", "ID"]:
        if key in data[0]:
            return key
    return None


def main():
    """Основная функция программы."""
    file_manager = FileManager()
    template_renderer = TemplateRenderer()
    # PDFGenerator создаем только когда нужно генерировать PDF
    pdf_generator: Optional[PDFGenerator] = None

    print("\n" + "=" * 60)
    print("  ГЕНЕРАТОР PDF ДОКУМЕНТОВ")
    print("=" * 60)

    # Получаем списки файлов
    data_files = file_manager.get_data_files()
    template_files = file_manager.get_template_files()

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
    Menu.print_menu(
        "Доступные файлы с данными",
        data_files,
        item_formatter=lambda f: f"{f.name} ({f.suffix.upper()})",
    )

    selected_data_file = Menu.get_user_choice(
        data_files, "Выберите файл с данными"
    )
    if not selected_data_file:
        return

    # Выводим меню выбора шаблона
    Menu.print_menu(
        "Доступные HTML шаблоны",
        template_files,
        item_formatter=lambda f: f.name,
    )

    selected_template = Menu.get_user_choice(
        template_files, "Выберите HTML шаблон"
    )
    if not selected_template:
        return

    # Загружаем данные и шаблон
    print(f"\nЗагрузка данных из {selected_data_file.name}...")
    try:
        data = file_manager.load_data_file(selected_data_file)
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return

    if not data:
        print("Ошибка: файл данных пуст или не содержит данных")
        return

    print(f"Загрузка шаблона {selected_template.name}...")
    template = file_manager.load_template(selected_template)

    # Извлекаем invoice_id из данных
    invoice_key = find_invoice_key(data)

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
    Menu.print_menu(
        "Доступные счета (invoices)",
        invoices,
        item_formatter=lambda item: f"ID: {item[1]}",
    )

    selected_invoice_index = Menu.get_user_choice(
        invoices, "Выберите invoice ID"
    )

    if not selected_invoice_index:
        return

    invoice_index = selected_invoice_index[0]
    invoice_data = data[invoice_index]

    # Генерируем PDF
    print(f"\nГенерация PDF для invoice ID: {selected_invoice_index[1]}...")

    try:
        # Ленивая загрузка PDFGenerator только когда нужно
        if pdf_generator is None:
            from pdfgenerator.core.generator import PDFGenerator

            pdf_generator = PDFGenerator()

        html_content = template_renderer.render(template, invoice_data)
        invoice_id = str(
            invoice_data.get(invoice_key, invoice_index + 1)
            if invoice_key
            else invoice_index + 1
        )
        safe_invoice_id = "".join(
            c for c in invoice_id if c.isalnum() or c in ("-", "_")
        )
        output_filename = f"invoice_{safe_invoice_id}.pdf"
        output_path = file_manager.get_output_path(output_filename)

        pdf_generator.generate(html_content, output_path)
        print(f"✓ PDF успешно создан: {output_path}")

        # Открываем PDF
        print("Открытие PDF...")
        pdf_generator.open_pdf(output_path)

    except Exception as e:
        print(f"Ошибка при генерации PDF: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

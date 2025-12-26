"""Генератор PDF документов."""

import os
import platform
from pathlib import Path

try:
    from weasyprint import CSS, HTML  # type: ignore
    from weasyprint.text.fonts import FontConfiguration  # type: ignore
except ImportError:
    print("Ошибка: библиотека WeasyPrint не установлена.")
    print("Установите её командой: pip install weasyprint")
    raise


class PDFGenerator:
    """Класс для генерации PDF документов."""

    def __init__(self):
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

    def generate(self, html_content: str, output_path: Path) -> None:
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

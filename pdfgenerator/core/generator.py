"""Генератор PDF документов."""

import os
import platform
import sys
from pathlib import Path
from typing import Any, Optional

# Глобальные переменные для ленивой загрузки WeasyPrint
_CSS: Optional[Any] = None
_HTML: Optional[Any] = None
_FontConfiguration: Optional[Any] = None


def _setup_macos_libraries() -> None:
    """Настроить пути к системным библиотекам для macOS."""
    if platform.system() != "Darwin":
        return

    # Проверяем, запущено ли приложение из PyInstaller bundle
    if getattr(sys, "frozen", False):
        # Если это собранное приложение, библиотеки должны быть в той же папке
        app_dir = os.path.dirname(sys.executable)
        if os.path.exists(app_dir):
            lib_paths = [app_dir]
        else:
            lib_paths = []
    else:
        lib_paths = []

    # Добавляем пути Homebrew
    brew_prefix = os.environ.get("HOMEBREW_PREFIX", "/opt/homebrew")
    if os.path.exists(f"{brew_prefix}/lib"):
        lib_paths.append(f"{brew_prefix}/lib")

    # Устанавливаем переменные окружения
    if lib_paths:
        lib_path = ":".join(lib_paths)
        if "DYLD_LIBRARY_PATH" in os.environ:
            os.environ["DYLD_LIBRARY_PATH"] = (
                f"{lib_path}:{os.environ['DYLD_LIBRARY_PATH']}"
            )
        else:
            os.environ["DYLD_LIBRARY_PATH"] = lib_path

        if "DYLD_FALLBACK_LIBRARY_PATH" in os.environ:
            os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
                f"{lib_path}:{os.environ['DYLD_FALLBACK_LIBRARY_PATH']}"
            )
        else:
            os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = lib_path


def _import_weasyprint() -> None:
    """Ленивый импорт WeasyPrint."""
    global _CSS, _HTML, _FontConfiguration

    if _CSS is not None:
        return  # Уже импортировано

    _setup_macos_libraries()

    try:
        from weasyprint import CSS, HTML  # type: ignore
        from weasyprint.text.fonts import FontConfiguration  # type: ignore

        _CSS = CSS
        _HTML = HTML
        _FontConfiguration = FontConfiguration
    except ImportError:
        print("Ошибка: библиотека WeasyPrint не установлена.")
        print("Установите её командой: pip install weasyprint")
        if platform.system() == "Darwin":
            print("\nТакже убедитесь, что установлены системные библиотеки:")
            print("brew install cairo pango gdk-pixbuf libffi glib")
            print("\nЕсли библиотеки установлены, но ошибка сохраняется,")
            print("попробуйте установить переменные окружения:")
            print("export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH")
        raise


class PDFGenerator:
    """Класс для генерации PDF документов."""

    def __init__(self):
        """Инициализация генератора (ленивая загрузка WeasyPrint)."""
        self._font_config: Optional[Any] = None
        self._css: Optional[Any] = None

    def _ensure_weasyprint(self) -> None:
        """Убедиться, что WeasyPrint загружен."""
        if self._font_config is None:
            _import_weasyprint()
            self._font_config = _FontConfiguration()
            self._css = _CSS(
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
                font_config=self._font_config,
            )

    def generate(self, html_content: str, output_path: Path) -> None:
        """Сгенерировать PDF из HTML контента."""
        self._ensure_weasyprint()
        _HTML(string=html_content).write_pdf(
            output_path, stylesheets=[self._css], font_config=self._font_config
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

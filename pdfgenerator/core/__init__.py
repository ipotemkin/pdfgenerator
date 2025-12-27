"""Основные модули для генерации PDF."""

from .file_manager import FileManager

# PDFGenerator импортируется лениво для ускорения запуска
# Импортируем только при необходимости
__all__ = ["FileManager"]

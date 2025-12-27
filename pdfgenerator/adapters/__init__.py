"""Адаптеры для чтения файлов разных форматов."""

from .base import DataAdapter
from .factory import get_adapter

# Адаптеры импортируются лениво в factory для ускорения запуска
__all__ = [
    "DataAdapter",
    "get_adapter",
]

"""Адаптеры для чтения файлов разных форматов."""

from .base import DataAdapter
from .csv_adapter import CSVAdapter
from .json_adapter import JSONAdapter
from .xlsx_adapter import XLSXAdapter
from .factory import get_adapter

__all__ = [
    "DataAdapter",
    "CSVAdapter",
    "JSONAdapter",
    "XLSXAdapter",
    "get_adapter",
]

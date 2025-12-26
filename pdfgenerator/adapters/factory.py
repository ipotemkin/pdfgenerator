"""Фабрика для создания адаптеров."""

from pathlib import Path

from .base import DataAdapter
from .csv_adapter import CSVAdapter
from .json_adapter import JSONAdapter
from .xlsx_adapter import XLSXAdapter


def get_adapter(file_path: Path) -> DataAdapter:
    """Получить подходящий адаптер для файла."""
    adapters: list[DataAdapter] = [
        JSONAdapter(),
        CSVAdapter(),
        XLSXAdapter(),
    ]

    for adapter in adapters:
        if adapter.can_read(file_path):
            return adapter

    raise ValueError(f"Неподдерживаемый формат файла: {file_path.suffix}")

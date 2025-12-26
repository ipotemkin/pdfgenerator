"""Адаптер для чтения CSV файлов."""

import csv
from pathlib import Path
from typing import Any, cast

from .base import DataAdapter

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class CSVAdapter(DataAdapter):
    """Адаптер для чтения CSV файлов."""

    @property
    def supported_extensions(self) -> list[str]:
        """Получить список поддерживаемых расширений."""
        return [".csv"]

    def can_read(self, file_path: Path) -> bool:
        """Проверить, может ли адаптер прочитать файл."""
        return file_path.suffix.lower() == ".csv"

    def read(self, file_path: Path) -> list[dict[str, Any]]:
        """Прочитать данные из CSV файла."""
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

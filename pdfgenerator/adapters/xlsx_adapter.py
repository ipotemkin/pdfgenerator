"""Адаптер для чтения XLSX файлов."""

from pathlib import Path
from typing import Any, cast

from .base import DataAdapter

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class XLSXAdapter(DataAdapter):
    """Адаптер для чтения XLSX файлов."""

    @property
    def supported_extensions(self) -> list[str]:
        """Получить список поддерживаемых расширений."""
        return [".xlsx"]

    def can_read(self, file_path: Path) -> bool:
        """Проверить, может ли адаптер прочитать файл."""
        return file_path.suffix.lower() == ".xlsx"

    def read(self, file_path: Path) -> list[dict[str, Any]]:
        """Прочитать данные из XLSX файла."""
        if not PANDAS_AVAILABLE:
            raise ImportError(
                "Для чтения XLSX файлов требуется pandas. "
                "Установите: pip install pandas openpyxl"
            )

        # Читаем первый лист Excel файла
        df = pd.read_excel(file_path, engine="openpyxl")
        records = df.to_dict("records")
        return cast(list[dict[str, Any]], records)

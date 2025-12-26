"""Адаптер для чтения JSON файлов."""

import json
from pathlib import Path
from typing import Any, cast

from .base import DataAdapter


class JSONAdapter(DataAdapter):
    """Адаптер для чтения JSON файлов."""

    @property
    def supported_extensions(self) -> list[str]:
        """Получить список поддерживаемых расширений."""
        return [".json"]

    def can_read(self, file_path: Path) -> bool:
        """Проверить, может ли адаптер прочитать файл."""
        return file_path.suffix.lower() == ".json"

    def read(self, file_path: Path) -> list[dict[str, Any]]:
        """Прочитать данные из JSON файла."""
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

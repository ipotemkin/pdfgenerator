"""Базовый класс для адаптеров чтения данных."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class DataAdapter(ABC):
    """Абстрактный базовый класс для адаптеров чтения данных."""

    @abstractmethod
    def can_read(self, file_path: Path) -> bool:
        """Проверить, может ли адаптер прочитать файл."""
        pass

    @abstractmethod
    def read(self, file_path: Path) -> list[dict[str, Any]]:
        """Прочитать данные из файла."""
        pass

    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Получить список поддерживаемых расширений файлов."""
        pass

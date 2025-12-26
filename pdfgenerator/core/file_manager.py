"""Менеджер для работы с файлами."""

from pathlib import Path
from typing import Any

from ..adapters import get_adapter


class FileManager:
    """Класс для управления файлами данных и шаблонов."""

    def __init__(
        self,
        data_dir: str = "data",
        templates_dir: str = "templates",
        output_dir: str = "output",
    ):
        self.data_dir = Path(data_dir)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)

        # Создаем директории, если их нет
        self.data_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

    def get_data_files(self) -> list[Path]:
        """Получить список всех файлов данных."""
        data_files: list[Path] = []
        if self.data_dir.exists():
            # Получаем все расширения из адаптеров
            from ..adapters import (
                CSVAdapter,
                JSONAdapter,
                XLSXAdapter,
            )

            adapters = [JSONAdapter(), CSVAdapter(), XLSXAdapter()]
            extensions = set()
            for adapter in adapters:
                extensions.update(adapter.supported_extensions)

            for ext in extensions:
                data_files.extend(self.data_dir.glob(f"*{ext}"))
        return sorted(data_files)

    def get_template_files(self) -> list[Path]:
        """Получить список всех HTML шаблонов."""
        templates = []
        if self.templates_dir.exists():
            templates = list(self.templates_dir.glob("*.html"))
        return sorted(templates)

    def load_data_file(self, file_path: Path) -> list[dict[str, Any]]:
        """Загрузить данные из файла."""
        adapter = get_adapter(file_path)
        return adapter.read(file_path)

    def load_template(self, template_path: Path) -> str:
        """Загрузить HTML шаблон."""
        with open(template_path, encoding="utf-8") as f:
            return f.read()

    def get_output_path(self, filename: str) -> Path:
        """Получить путь для сохранения выходного файла."""
        return self.output_dir / filename

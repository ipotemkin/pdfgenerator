# PDF Generator - CLI утилита для генерации PDF

CLI-утилита для генерации PDF документов из данных (CSV/JSON/XLSX) и HTML-шаблонов.

## Структура проекта

Проект организован в модульную структуру для легкого расширения и поддержки:

```
pdfgenerator/
├── adapters/          # Адаптеры для чтения файлов разных форматов
│   ├── base.py        # Базовый класс адаптера
│   ├── csv_adapter.py # Адаптер для CSV
│   ├── json_adapter.py# Адаптер для JSON
│   ├── xlsx_adapter.py# Адаптер для XLSX
│   └── factory.py     # Фабрика для создания адаптеров
├── core/              # Основные модули
│   ├── generator.py   # Генератор PDF
│   └── file_manager.py# Менеджер файлов
├── templates/         # Работа с шаблонами
│   └── renderer.py    # Рендерер HTML шаблонов
└── ui/                # Пользовательский интерфейс
    └── menu.py        # Консольное меню
```

## Установка

### Установка через pipx (рекомендуется)

pipx устанавливает приложение в изолированное окружение и создает глобальную команду `pdfgenerator`:

```bash
# Установите pipx, если еще не установлен
# macOS/Linux:
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Или через Homebrew (macOS):
brew install pipx

# Установите приложение из текущей директории:
pipx install .

# Или установите из Git репозитория:
# pipx install git+https://github.com/yourusername/pdfchecker.git
```

После установки вы можете запускать приложение просто командой:
```bash
pdfgenerator
```

**Обновление приложения:**
```bash
pipx upgrade pdfgenerator
```

**Удаление приложения:**
```bash
pipx uninstall pdfgenerator
```

### Установка через pip (для разработки)

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Убедитесь, что у вас установлены системные зависимости для WeasyPrint:
   - **macOS**: `brew install cairo pango gdk-pixbuf libffi glib`
   - **Windows**: WeasyPrint должен работать из коробки
   - **Linux**: `sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0`

## Использование

1. Поместите файлы с данными (CSV, JSON или XLSX) в директорию `data/`
2. Поместите HTML-шаблоны в директорию `templates/`
3. Запустите скрипт:
```bash
# Если установлено через pipx:
pdfgen

# Или напрямую через Python:
python main.py
```

**Примечание:** Приложение оптимизировано для быстрого запуска. Тяжелые библиотеки (WeasyPrint, pandas) загружаются только когда они действительно нужны, что ускоряет старт приложения примерно в 6 раз.

4. Следуйте инструкциям в консоли:
   - Выберите файл с данными
   - Выберите HTML-шаблон
   - Выберите invoice ID
   - PDF будет автоматически сгенерирован и открыт

## Сборка исполняемого файла

Проект включает Makefile для сборки исполняемых файлов для разных платформ.

**Важно:** WeasyPrint требует системные библиотеки (cairo, pango, gobject), которые не могут быть полностью включены в один исполняемый файл. Рекомендуется использовать сборку в папку (`--onedir`) вместо одного файла (`--onefile`).

### Установка инструментов сборки

```bash
make install
```

Это установит все зависимости, включая PyInstaller.

### Сборка для текущей ОС

Запускается под работающим виртуальным окуржением!!!

**Рекомендуется (сборка в папку):**
```bash
make build-dir
```

**Альтернатива (один файл, может не работать):**
```bash
make build
```

### Сборка для конкретной платформы

**macOS:**
```bash
make build-macos      # Сборка исполняемого файла
```

**Linux:**
```bash
make build-linux
```

**Windows:**
```bash
make build-windows  # Для Windows (требуется Linux с wine или Windows)
```

### Требования для работы исполняемого файла

Запускается из системы без активации виртуального окружения.

Исполняемый файл требует установки системных библиотек на целевой машине:

- **macOS**: `brew install cairo pango gdk-pixbuf libffi glib`
- **Linux**: `sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0`
- **Windows**: Обычно работает из коробки, но может потребоваться установка GTK+

### Очистка временных файлов

```bash
make clean
```

### Решение проблем со сборкой

Если при запуске исполняемого файла возникает ошибка:
```
OSError: cannot load library 'libgobject-2.0-0'
```

Это означает, что системные библиотеки WeasyPrint не найдены. Решения:

1. **Используйте сборку в папку** (`make build-dir`) вместо одного файла

2. **Установите системные библиотеки** на целевой машине:
   - macOS: `brew install cairo pango gdk-pixbuf libffi glib glib`
   - Linux: `sudo apt-get install libcairo2 libpango-1.0-0 libgobject-2.0-0`

3. **Установите переменные окружения** (macOS):
   ```bash
   export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
   export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH
   ./dist/pdfgenerator/pdfgenerator
   ```

4. **Используйте Python напрямую** вместо исполняемого файла: `python main.py`
   - Это самый надежный способ, так как Python может найти все библиотеки автоматически

## Проверка кода

Проект включает скрипт `check.sh` для проверки качества кода:

```bash
./check.sh
```

Или через Makefile:

```bash
make check
```

Скрипт выполняет:
1. **Black** - форматирование кода
2. **mypy** - проверка типов
3. **ruff** - линтинг и исправление ошибок

### Ручная проверка

Вы также можете запустить инструменты вручную:

```bash
# Форматирование
black .

# Проверка типов
mypy . --exclude "backup|venv|.venv|sandbox|migrations|tests|nogit|prompts|data|templates"

# Линтинг
ruff check . --fix
```

## Структура данных

### JSON формат
```json
[
  {
    "invoice_id": "INV-001",
    "date": "2024-01-15",
    "customer_name": "Иван Петров",
    "items": [
      {"name": "Товар 1", "quantity": 2, "price": 1500.00}
    ],
    "total": 3000.00,
    "tax": 600.00,
    "grand_total": 3600.00
  }
]
```

### CSV формат
CSV файлы должны содержать колонки с данными. Каждая строка представляет отдельный invoice.

### XLSX формат
XLSX (Excel) файлы поддерживаются через библиотеку pandas и openpyxl. Файл должен содержать таблицу с данными, где каждая строка представляет отдельный invoice. Первая строка должна содержать заголовки колонок. Читается первый лист файла.

## HTML шаблоны

HTML шаблоны используют стандартный Python форматирование строк:
- `{invoice_id}` - подставит значение invoice_id
- `{customer_name}` - подставит имя клиента
- `{items_html}` - автоматически сгенерированная HTML таблица с товарами
- `{total:.2f}` - форматирование чисел (например, для суммы)

Примеры шаблонов находятся в директории `templates/`.

## Расширение функционала

Проект спроектирован для легкого расширения:

### Добавление нового формата файлов

1. Создайте новый адаптер в `pdfgenerator/adapters/`:
```python
from .base import DataAdapter

class NewFormatAdapter(DataAdapter):
    @property
    def supported_extensions(self) -> list[str]:
        return [".newformat"]
    
    def can_read(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == ".newformat"
    
    def read(self, file_path: Path) -> list[dict[str, Any]]:
        # Ваша логика чтения
        pass
```

2. Зарегистрируйте адаптер в `pdfgenerator/adapters/factory.py`

### Добавление новых функций UI

Добавьте новые методы в класс `Menu` в `pdfgenerator/ui/menu.py`

## Выходные файлы

Сгенерированные PDF файлы сохраняются в директории `output/` с именем `invoice_{invoice_id}.pdf`.

## Разработка

### Структура модулей

- **adapters** - Адаптеры для чтения различных форматов файлов (расширяемо)
- **core** - Основная логика приложения (генерация PDF, управление файлами)
- **templates** - Рендеринг HTML шаблонов
- **ui** - Пользовательский интерфейс (консольное меню)

### Требования для разработки

Дополнительные зависимости для разработки находятся в `requrements-dev.txt`:
- black (форматирование)
- mypy (проверка типов)
- ruff (линтинг)

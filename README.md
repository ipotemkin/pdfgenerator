# PDF Generator - CLI утилита для генерации PDF

CLI-утилита для генерации PDF документов из данных (CSV/JSON) и HTML-шаблонов.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Убедитесь, что у вас установлены системные зависимости для WeasyPrint:
   - **macOS**: `brew install cairo pango gdk-pixbuf libffi`
   - **Windows**: WeasyPrint должен работать из коробки
   - **Linux**: `sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0`

## Использование

1. Поместите файлы с данными (CSV или JSON) в директорию `data/`
2. Поместите HTML-шаблоны в директорию `templates/`
3. Запустите скрипт:
```bash
python pdf_generator.py
```

4. Следуйте инструкциям в консоли:
   - Выберите файл с данными
   - Выберите HTML-шаблон
   - Выберите invoice ID
   - PDF будет автоматически сгенерирован и открыт

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

## HTML шаблоны

HTML шаблоны используют стандартный Python форматирование строк:
- `{invoice_id}` - подставит значение invoice_id
- `{customer_name}` - подставит имя клиента
- `{items_html}` - автоматически сгенерированная HTML таблица с товарами

Примеры шаблонов находятся в директории `templates/`.

## Выходные файлы

Сгенерированные PDF файлы сохраняются в директории `output/` с именем `invoice_{invoice_id}.pdf`.


.PHONY: help install install-pipx build build-dir clean test check build-windows build-linux build-macos

# Переменные
PYTHON := python3
PIP := pip3
APP_NAME := pdfgenerator
MAIN_FILE := main.py

help:
	@echo "Доступные команды:"
	@echo "  make install        - Установить зависимости"
	@echo "  make install-pipx   - Установить через pipx (рекомендуется)"
	@echo "  make build          - Собрать один исполняемый файл (может не работать с WeasyPrint)"
	@echo "  make build-dir      - Собрать в папку (рекомендуется для WeasyPrint)"
	@echo "  make build-windows  - Собрать исполняемый файл для Windows"
	@echo "  make build-linux    - Собрать исполняемый файл для Linux"
	@echo "  make build-macos    - Собрать исполняемый файл для macOS"
	@echo "  make clean          - Очистить временные файлы"
	@echo "  make check          - Проверить код (black, mypy, ruff)"
	@echo "  make test           - Запустить тесты"

install:
	$(PIP) install -r requirements.txt
	$(PIP) install pyinstaller

install-pipx:
	@echo "Установка через pipx..."
	@if ! command -v pipx >/dev/null 2>&1; then \
		echo "pipx не установлен. Установите его:"; \
		echo "  python3 -m pip install --user pipx"; \
		echo "  python3 -m pipx ensurepath"; \
		echo "Или через Homebrew: brew install pipx"; \
		exit 1; \
	fi
	pipx install .
	@echo "Приложение установлено! Запустите командой: pdfgenerator"

build: install
	@echo "Сборка для текущей ОС (один файл)..."
	@echo "Внимание: сборка одного файла может не работать из-за системных библиотек WeasyPrint."
	@echo "Рекомендуется использовать 'make build-dir' для более надежной сборки."
	pyinstaller --onefile --name $(APP_NAME) \
		--add-data "pdfgenerator:pdfgenerator" \
		--collect-all weasyprint \
		--collect-submodules weasyprint \
		--hidden-import=weasyprint \
		--hidden-import=pandas \
		--hidden-import=openpyxl \
		--hidden-import=cffi \
		--hidden-import=fontTools \
		--hidden-import=PIL \
		$(MAIN_FILE)
	@echo "Исполняемый файл создан в dist/$(APP_NAME)"

build-dir: install
	@echo "Сборка для текущей ОС (папка) - рекомендуется..."
	pyinstaller --onedir --name $(APP_NAME) \
		--add-data "pdfgenerator:pdfgenerator" \
		--collect-all weasyprint \
		--collect-submodules weasyprint \
		--hidden-import=weasyprint \
		--hidden-import=pandas \
		--hidden-import=openpyxl \
		--hidden-import=cffi \
		--hidden-import=fontTools \
		--hidden-import=PIL \
		$(MAIN_FILE)
	@echo "Приложение создано в dist/$(APP_NAME)/"
	@echo "Запуск: ./dist/$(APP_NAME)/$(APP_NAME)"

build-windows: install
	@echo "Сборка для Windows..."
	@if [ "$$(uname)" != "Linux" ]; then \
		echo "Для сборки Windows версии требуется Linux с wine или Windows"; \
		exit 1; \
	fi
	pyinstaller --onefile --name $(APP_NAME).exe \
		--add-data "pdfgenerator;pdfgenerator" \
		--collect-all weasyprint \
		--collect-submodules weasyprint \
		--hidden-import=weasyprint \
		--hidden-import=pandas \
		--hidden-import=openpyxl \
		--hidden-import=cffi \
		--hidden-import=fontTools \
		--hidden-import=PIL \
		--target-arch=win64 \
		$(MAIN_FILE)
	@echo "Исполняемый файл создан в dist/$(APP_NAME).exe"

build-linux: install
	@echo "Сборка для Linux..."
	@if [ "$$(uname)" != "Linux" ]; then \
		echo "Для сборки Linux версии требуется Linux"; \
		exit 1; \
	fi
	@echo "Внимание: для работы WeasyPrint в исполняемом файле Linux требуются системные библиотеки."
	@echo "Убедитесь, что установлены: sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0"
	pyinstaller --onefile --name $(APP_NAME) \
		--add-data "pdfgenerator:pdfgenerator" \
		--collect-all weasyprint \
		--collect-submodules weasyprint \
		--hidden-import=weasyprint \
		--hidden-import=pandas \
		--hidden-import=openpyxl \
		--hidden-import=cffi \
		--hidden-import=fontTools \
		--hidden-import=PIL \
		$(MAIN_FILE)
	@echo "Исполняемый файл создан в dist/$(APP_NAME)"

build-macos: install
	@echo "Сборка для macOS (один файл)..."
	@if [ "$$(uname)" != "Darwin" ]; then \
		echo "Для сборки macOS версии требуется macOS"; \
		exit 1; \
	fi
	@echo "Внимание: сборка одного файла может не работать из-за системных библиотек WeasyPrint."
	pyinstaller --onefile --name $(APP_NAME) \
		--add-data "pdfgenerator:pdfgenerator" \
		--collect-all weasyprint \
		--collect-submodules weasyprint \
		--hidden-import=weasyprint \
		--hidden-import=pandas \
		--hidden-import=openpyxl \
		--hidden-import=cffi \
		--hidden-import=fontTools \
		--hidden-import=PIL \
		--collect-binaries cffi \
		$(MAIN_FILE)
	@echo "Исполняемый файл создан в dist/$(APP_NAME)"
	@echo "Примечание: для работы на других Mac может потребоваться установка системных библиотек"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.spec
	rm -rf __pycache__/
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

check:
	@echo "Проверка кода..."
	@./check.sh

test:
	@echo "Запуск тестов..."
	@echo "Тесты пока не реализованы"


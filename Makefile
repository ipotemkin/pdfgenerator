.PHONY: help install build clean test check build-windows build-linux build-macos

# Переменные
PYTHON := python3
PIP := pip3
APP_NAME := pdfgenerator
MAIN_FILE := main.py

help:
	@echo "Доступные команды:"
	@echo "  make install     - Установить зависимости"
	@echo "  make build       - Собрать исполняемый файл для текущей ОС"
	@echo "  make build-windows - Собрать исполняемый файл для Windows"
	@echo "  make build-linux   - Собрать исполняемый файл для Linux"
	@echo "  make build-macos   - Собрать исполняемый файл для macOS"
	@echo "  make clean       - Очистить временные файлы"
	@echo "  make check       - Проверить код (black, mypy, ruff)"
	@echo "  make test        - Запустить тесты"

install:
	$(PIP) install -r requirements.txt
	$(PIP) install pyinstaller

build: install
	@echo "Сборка для текущей ОС..."
	pyinstaller --onefile --name $(APP_NAME) \
		--add-data "pdfgenerator:pdfgenerator" \
		--hidden-import=weasyprint \
		--hidden-import=pandas \
		--hidden-import=openpyxl \
		$(MAIN_FILE)
	@echo "Исполняемый файл создан в dist/$(APP_NAME)"

build-windows: install
	@echo "Сборка для Windows..."
	@if [ "$$(uname)" != "Linux" ]; then \
		echo "Для сборки Windows версии требуется Linux с wine или Windows"; \
		exit 1; \
	fi
	pyinstaller --onefile --name $(APP_NAME).exe \
		--add-data "pdfgenerator:pdfgenerator" \
		--hidden-import=weasyprint \
		--hidden-import=pandas \
		--hidden-import=openpyxl \
		--target-arch=win64 \
		$(MAIN_FILE)
	@echo "Исполняемый файл создан в dist/$(APP_NAME).exe"

build-linux: install
	@echo "Сборка для Linux..."
	@if [ "$$(uname)" != "Linux" ]; then \
		echo "Для сборки Linux версии требуется Linux"; \
		exit 1; \
	fi
	pyinstaller --onefile --name $(APP_NAME) \
		--add-data "pdfgenerator:pdfgenerator" \
		--hidden-import=weasyprint \
		--hidden-import=pandas \
		--hidden-import=openpyxl \
		$(MAIN_FILE)
	@echo "Исполняемый файл создан в dist/$(APP_NAME)"

build-macos: install
	@echo "Сборка для macOS..."
	@if [ "$$(uname)" != "Darwin" ]; then \
		echo "Для сборки macOS версии требуется macOS"; \
		exit 1; \
	fi
	pyinstaller --onefile --name $(APP_NAME) \
		--add-data "pdfgenerator:pdfgenerator" \
		--hidden-import=weasyprint \
		--hidden-import=pandas \
		--hidden-import=openpyxl \
		$(MAIN_FILE)
	@echo "Исполняемый файл создан в dist/$(APP_NAME)"

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


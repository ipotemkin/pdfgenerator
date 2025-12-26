#!/usr/bin/env bash

set -e

echo "formatting with black..."
black .

echo "checking with mypy..."
mypy . --exclude "backup|venv|.venv|sandbox|migrations|tests|nogit|prompts|data|templates"

echo "checking with ruff..."
ruff check . --fix

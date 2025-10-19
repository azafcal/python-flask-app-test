# Makefile for Flask Todo App
# Provides convenient commands for testing, development, and deployment

.PHONY: help install test test-unit test-integration test-api test-slow test-fast test-parallel coverage lint format clean run dev

# Default target
help:
	@echo "Flask Todo App - Available commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install dependencies with uv"
	@echo "  make install-dev   Install dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run all tests"
	@echo "  make test-unit     Run unit tests only"
	@echo "  make test-integration  Run integration tests only"
	@echo "  make test-api      Run API tests only"
	@echo "  make test-slow     Run slow/performance tests"
	@echo "  make test-fast     Run fast tests (exclude slow)"
	@echo "  make test-parallel Run tests in parallel"
	@echo "  make coverage      Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          Run linting tools"
	@echo "  make format        Format code with black and isort"
	@echo "  make check         Run all quality checks"
	@echo ""
	@echo "Development:"
	@echo "  make run           Run the application"
	@echo "  make dev           Run in development mode"
	@echo "  make clean         Clean up generated files"

# Installation targets
install:
	uv sync

install-dev:
	uv sync --extra dev

# Test targets
test:
	uv run pytest -v

test-unit:
	uv run pytest -m unit -v

test-integration:
	uv run pytest -m integration -v

test-api:
	uv run pytest -m api -v

test-slow:
	uv run pytest -m slow -v

test-fast:
	uv run pytest -m "not slow" -v

test-parallel:
	uv run pytest -n 4 -v

coverage:
	uv run pytest --cov=src/flask_todo_app --cov-report=html --cov-report=term --cov-report=xml -v
	@echo "Coverage report generated in htmlcov/"

# Code quality targets
lint:
	uv run flake8 src/ tests/
	uv run black --check src/ tests/
	uv run isort --check-only src/ tests/

format:
	uv run black src/ tests/
	uv run isort src/ tests/

type-check:
	uv run mypy src/

check: lint type-check
	@echo "All quality checks passed!"

# Development targets
run:
	uv run python src/flask_todo_app/app.py

dev:
	uv run python -m flask --app src/flask_todo_app/app.py run --debug

# Utility targets
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf reports/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Database targets
init-db:
	uv run python -c "from src.flask_todo_app.app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"

reset-db:
	rm -f test.db
	make init-db

# Docker targets (if using Docker in the future)
docker-build:
	docker build -t flask-todo-app .

docker-run:
	docker run -p 5000:5000 flask-todo-app

# CI/CD simulation
ci: install-dev lint type-check coverage
	@echo "CI pipeline completed successfully!"

# Generate test reports
report:
	mkdir -p reports
	uv run pytest --html=reports/report.html --self-contained-html
	@echo "Test report generated in reports/report.html"

# Performance testing
perf-test:
	uv run pytest -m slow --tb=short -v

# Security scanning (placeholder for future security tools)
security:
	@echo "Security scanning not yet implemented"

# Dependency management
update-deps:
	uv sync --upgrade

# Show project info
info:
	@echo "Project: Flask Todo Application"
	@echo "Python version: $(shell python --version)"
	@echo "UV version: $(shell uv --version)"
	@echo "Project structure:"
	@tree -I '__pycache__|*.pyc|.pytest_cache|htmlcov|.venv' -L 3
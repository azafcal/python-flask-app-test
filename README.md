# Flask Todo Application with Comprehensive Testing

A Flask-based todo application with a comprehensive testing suite using `uv` for modern Python environment management.

## 🚀 Features

- ✅ CRUD operations for todos
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Prometheus metrics integration
- ✅ Comprehensive test suite with multiple test types
- ✅ Modern Python packaging with `uv`
- ✅ Code quality tools (black, flake8, isort, mypy)
- ✅ Test coverage reporting
- ✅ CI/CD ready

## 📁 Project Structure

```
flask-todo-app/
├── src/
│   └── flask_todo_app/
│       ├── __init__.py
│       └── app.py              # Main Flask application
├── tests/
│   ├── conftest.py             # Shared test fixtures
│   ├── unit/
│   │   └── test_models.py      # Unit tests for models
│   ├── integration/
│   │   ├── test_routes.py      # Integration tests for routes
│   │   ├── test_api.py         # API endpoint tests
│   │   └── test_performance.py # Performance and load tests
│   └── fixtures/
│       └── factories.py        # Test data factories
├── scripts/
│   └── test.py                 # Test runner script
├── pyproject.toml              # Project configuration
├── Makefile                    # Convenient commands
└── README.md
```

## 🛠️ Setup (Modern with UV)

### Prerequisites
- Python 3.9+
- `uv` package manager (auto-installed if needed)

### Installation

1. **Install dependencies:**
   ```bash
   make install-dev
   # or manually:
   uv sync --extra dev
   ```

2. **Initialize the database:**
   ```bash
   make init-db
   ```

3. **Run tests to verify setup:**
   ```bash
   make test-fast
   ```

## 🧪 Testing

This project includes a comprehensive testing suite with different types of tests:

### Test Types

1. **Unit Tests** (`pytest -m unit`)
   - Test individual components in isolation
   - Fast execution
   - Focus on model logic and business rules

2. **Integration Tests** (`pytest -m integration`)
   - Test component interactions
   - Database operations
   - HTTP endpoints

3. **API Tests** (`pytest -m api`)
   - Test API endpoints (future-ready)
   - JSON handling
   - Prometheus metrics

4. **Performance Tests** (`pytest -m slow`)
   - Load testing
   - Concurrent operations
   - Memory usage monitoring

### Running Tests

#### Using Make (Recommended)

```bash
# Run all tests
make test

# Run specific test types
make test-unit          # Unit tests only
make test-integration   # Integration tests only
make test-api          # API tests only
make test-slow         # Performance tests
make test-fast         # All except slow tests

# Run with coverage
make coverage

# Run tests in parallel
make test-parallel

# Generate HTML test report
make report
```

#### Using UV Directly

```bash
# Run all tests
uv run pytest

# Run specific test types
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m "not slow"

# Run with coverage
uv run pytest --cov=src/flask_todo_app --cov-report=html

# Run in parallel
uv run pytest -n 4
```

## 🔧 Development

### Running the Application

```bash
# Production mode
make run

# Development mode with auto-reload
make dev

# Direct execution
uv run python src/flask_todo_app/app.py
```

### Code Quality

```bash
# Check code quality
make lint

# Format code
make format

# Type checking
make type-check

# Run all quality checks
make check
```

## 🐳 Docker (Legacy Support)

1. Install Docker
```
https://docs.docker.com/engine/install/
```

2. Run:
```bash
$ docker compose up --build #To see the logs
```
or:
```bash
$ docker compose up -d --build #To avoid seeing the logs
```

Access the API at http://localhost:5000 and Prometheus at http://localhost:9090.

## Contributing

Since this is a repository for a tutorial, the code should remain the same as the code that was shown in the tutorial. Any pull requests that don't address security flaws or fixes for language updates will be automatically closed. Style changes, adding libraries, etc are not valid changes for submitting a pull request.

## References:
- https://github.com/jakerieger/FlaskIntroduction.git
- https://medium.com/@letathenasleep/exposing-python-metrics-with-prometheus-c5c837c21e4d
- https://medium.com/@abderraoufbenchoubane/setup-a-python-environment-with-docker-a4e38811e0d3
- https://stackoverflow.com/questions/17042201/how-to-style-input-and-submit-button-with-css

..thanks!

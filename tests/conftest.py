"""
Shared test configuration and fixtures for the Flask Todo App.

This file contains pytest fixtures that are available across all test modules.
"""

import os
import tempfile
import pytest
from datetime import datetime
from unittest.mock import patch

# Add src to path so we can import the app
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flask_todo_app.app import app, db, Todo


@pytest.fixture(scope="session")
def app_instance():
    """Create and configure a new app instance for the entire test session."""
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })
    return app


@pytest.fixture
def client(app_instance):
    """Create a test client with a temporary database."""
    db_fd, db_path = tempfile.mkstemp()
    app_instance.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    with app_instance.test_client() as client:
        with app_instance.app_context():
            db.create_all()
        yield client
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def app_context(app_instance):
    """Provide an application context for tests that need it."""
    db_fd, db_path = tempfile.mkstemp()
    app_instance.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    with app_instance.app_context():
        db.create_all()
        yield app_instance
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def sample_todo():
    """Create a sample Todo instance for testing."""
    return Todo(content="Sample Todo Task", date_created=datetime.utcnow())


@pytest.fixture
def populated_db(app_context):
    """Create a database with sample data."""
    todos = [
        Todo(content="First Task"),
        Todo(content="Second Task"),
        Todo(content="Third Task"),
    ]
    
    for todo in todos:
        db.session.add(todo)
    db.session.commit()
    
    return todos


# Mock fixtures can be added here for more advanced testing scenarios

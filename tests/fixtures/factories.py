"""
Test data factories using factory-boy.

These factories help create test data for more complex testing scenarios.
"""

import factory
from factory import fuzzy
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from flask_todo_app.app import Todo, db


class TodoFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Todo instances."""
    
    class Meta:
        model = Todo
        sqlalchemy_session_persistence = "commit"
    
    id = factory.Sequence(lambda n: n)
    content = factory.Faker('text', max_nb_chars=100)
    date_created = factory.LazyFunction(datetime.utcnow)


class TodoFactoryWithCustomContent(TodoFactory):
    """Todo factory with specific content patterns."""
    
    content = factory.Faker('sentence', nb_words=4)


class TodoFactoryWithOldDate(TodoFactory):
    """Todo factory with older creation dates."""
    
    date_created = factory.LazyFunction(
        lambda: datetime.utcnow() - timedelta(days=factory.fuzzy.FuzzyInteger(1, 30).fuzz())
    )


class TodoFactoryWithLongContent(TodoFactory):
    """Todo factory with longer content for testing limits."""
    
    content = factory.Faker('text', max_nb_chars=500)


class TodoFactoryWithSpecialChars(TodoFactory):
    """Todo factory with special characters for testing encoding."""
    
    content = factory.LazyAttribute(
        lambda obj: f"Special chars: áéíóú ñÑ @#$%&*()[] - {factory.Faker('word').evaluate(None, None, {'locale': None})}"
    )


def create_todo_batch(count=5, factory_class=TodoFactory, **kwargs):
    """
    Create a batch of todos using the specified factory.
    
    Args:
        count (int): Number of todos to create
        factory_class: Factory class to use
        **kwargs: Additional attributes to pass to the factory
    
    Returns:
        list: List of created Todo instances
    """
    return factory_class.create_batch(count, **kwargs)


def create_mixed_todos():
    """Create a diverse set of todos for comprehensive testing."""
    todos = []
    
    # Regular todos
    todos.extend(create_todo_batch(3, TodoFactory))
    
    # Todos with long content
    todos.extend(create_todo_batch(2, TodoFactoryWithLongContent))
    
    # Todos with special characters
    todos.extend(create_todo_batch(2, TodoFactoryWithSpecialChars))
    
    # Old todos
    todos.extend(create_todo_batch(3, TodoFactoryWithOldDate))
    
    return todos
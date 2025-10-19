"""
Unit tests for the Todo model.

These tests focus on the Todo model behavior in isolation.
"""

import pytest
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from flask_todo_app.app import Todo, db


class TestTodoModel:
    """Unit tests for the Todo model."""

    @pytest.mark.unit
    def test_todo_creation(self, app_context):
        """Test creating a new Todo instance."""
        todo = Todo(content="Test task")
        
        assert todo.content == "Test task"
        assert todo.id is None  # Not saved yet
        # date_created is set when object is committed to database
        assert todo.date_created is None or isinstance(todo.date_created, datetime)
    
    @pytest.mark.unit
    def test_todo_creation_with_explicit_date(self, app_context):
        """Test creating a todo with explicit date."""
        test_date = datetime.utcnow()
        todo = Todo(content="Test task", date_created=test_date)
        
        assert todo.content == "Test task"
        assert todo.date_created == test_date
        assert isinstance(todo.date_created, datetime)

    @pytest.mark.unit
    def test_todo_repr(self, app_context):
        """Test the string representation of a Todo instance."""
        todo = Todo(content="Test task")
        db.session.add(todo)
        db.session.commit()
        
        expected_repr = f"<Task {todo.id}>"
        assert repr(todo) == expected_repr

    @pytest.mark.unit
    @pytest.mark.database
    def test_todo_database_save(self, app_context):
        """Test saving a Todo to the database."""
        todo = Todo(content="Task to save")
        db.session.add(todo)
        db.session.commit()
        
        # Verify it was saved
        saved_todo = Todo.query.filter_by(content="Task to save").first()
        assert saved_todo is not None
        assert saved_todo.content == "Task to save"
        assert saved_todo.id is not None
        assert isinstance(saved_todo.date_created, datetime)

    @pytest.mark.unit
    @pytest.mark.database
    def test_todo_query_all(self, app_context):
        """Test querying all todos."""
        # Create multiple todos
        todos = [
            Todo(content="First task"),
            Todo(content="Second task"),
            Todo(content="Third task"),
        ]
        
        for todo in todos:
            db.session.add(todo)
        db.session.commit()
        
        all_todos = Todo.query.all()
        assert len(all_todos) == 3
        
        contents = [todo.content for todo in all_todos]
        assert "First task" in contents
        assert "Second task" in contents
        assert "Third task" in contents

    @pytest.mark.unit
    @pytest.mark.database
    def test_todo_ordering(self, app_context):
        """Test that todos are ordered by creation date."""
        # Create todos with slight delay to ensure different timestamps
        import time
        
        first_todo = Todo(content="First")
        db.session.add(first_todo)
        db.session.commit()
        
        time.sleep(0.01)
        
        second_todo = Todo(content="Second")
        db.session.add(second_todo)
        db.session.commit()
        
        # Query ordered by date_created
        ordered_todos = Todo.query.order_by(Todo.date_created).all()
        
        assert len(ordered_todos) == 2
        assert ordered_todos[0].content == "First"
        assert ordered_todos[1].content == "Second"
        assert ordered_todos[0].date_created < ordered_todos[1].date_created

    @pytest.mark.unit
    @pytest.mark.database
    def test_todo_deletion(self, app_context):
        """Test deleting a todo from the database."""
        todo = Todo(content="Task to delete")
        db.session.add(todo)
        db.session.commit()
        
        todo_id = todo.id
        
        # Delete the todo
        db.session.delete(todo)
        db.session.commit()
        
        # Verify it's deleted
        deleted_todo = Todo.query.get(todo_id)
        assert deleted_todo is None

    @pytest.mark.unit
    def test_todo_with_empty_content(self, app_context):
        """Test creating a todo with empty content."""
        todo = Todo(content="")
        
        assert todo.content == ""
        # date_created is set when object is committed to database
        assert todo.date_created is None or isinstance(todo.date_created, datetime)

    @pytest.mark.unit
    def test_todo_with_long_content(self, app_context):
        """Test creating a todo with long content."""
        long_content = "A" * 300  # Longer than typical content
        todo = Todo(content=long_content)
        
        assert todo.content == long_content
        assert len(todo.content) == 300
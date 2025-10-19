"""
Integration tests for Flask application routes.

These tests verify that the routes work correctly with the database
and handle HTTP requests properly.
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from flask_todo_app.app import Todo, db


class TestIndexRoute:
    """Tests for the index route (/)."""

    @pytest.mark.integration
    def test_index_get_empty_database(self, client):
        """Test GET / with no todos in database."""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'<html' in response.data.lower()

    @pytest.mark.integration
    def test_index_get_with_existing_todos(self, client, populated_db):
        """Test GET / with existing todos."""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'First Task' in response.data
        assert b'Second Task' in response.data
        assert b'Third Task' in response.data

    @pytest.mark.integration
    def test_index_post_create_todo(self, client):
        """Test POST / to create a new todo."""
        response = client.post('/', 
                             data={'content': 'New todo from test'}, 
                             follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify todo was created in database
        with client.application.app_context():
            todo = Todo.query.filter_by(content='New todo from test').first()
            assert todo is not None
            assert todo.content == 'New todo from test'

    @pytest.mark.integration
    def test_index_post_empty_content(self, client):
        """Test POST / with empty content."""
        response = client.post('/', 
                             data={'content': ''}, 
                             follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify empty todo was created (current app behavior)
        with client.application.app_context():
            todo = Todo.query.filter_by(content='').first()
            assert todo is not None

    @pytest.mark.integration
    def test_index_post_whitespace_content(self, client):
        """Test POST / with whitespace-only content."""
        response = client.post('/', 
                             data={'content': '   '}, 
                             follow_redirects=True)
        
        assert response.status_code == 200
        
        with client.application.app_context():
            todo = Todo.query.filter_by(content='   ').first()
            assert todo is not None

    @pytest.mark.integration
    def test_index_post_long_content(self, client):
        """Test POST / with very long content."""
        long_content = "Very long todo content " * 50
        response = client.post('/', 
                             data={'content': long_content}, 
                             follow_redirects=True)
        
        assert response.status_code == 200
        
        with client.application.app_context():
            todo = Todo.query.filter_by(content=long_content).first()
            assert todo is not None

    @pytest.mark.integration
    def test_index_post_special_characters(self, client):
        """Test POST / with special characters in content."""
        special_content = "Todo with special chars: áéíóú ñÑ @#$%&*()[]"
        response = client.post('/', 
                             data={'content': special_content}, 
                             follow_redirects=True)
        
        assert response.status_code == 200
        
        with client.application.app_context():
            todo = Todo.query.filter_by(content=special_content).first()
            assert todo is not None


class TestDeleteRoute:
    """Tests for the delete route (/delete/<id>)."""

    @pytest.mark.integration
    def test_delete_existing_todo(self, client):
        """Test deleting an existing todo."""
        # Create a todo first
        with client.application.app_context():
            todo = Todo(content="Todo to delete")
            db.session.add(todo)
            db.session.commit()
            todo_id = todo.id
        
        # Delete the todo
        response = client.get(f'/delete/{todo_id}', follow_redirects=True)
        assert response.status_code == 200
        
        # Verify it was deleted
        with client.application.app_context():
            deleted_todo = Todo.query.get(todo_id)
            assert deleted_todo is None

    @pytest.mark.integration
    def test_delete_nonexistent_todo(self, client):
        """Test deleting a todo that doesn't exist."""
        response = client.get('/delete/9999')
        assert response.status_code == 404

    @pytest.mark.integration
    def test_delete_invalid_id(self, client):
        """Test deleting with invalid ID format."""
        response = client.get('/delete/invalid')
        assert response.status_code == 404


class TestUpdateRoute:
    """Tests for the update route (/update/<id>)."""

    @pytest.mark.integration
    def test_update_get_existing_todo(self, client):
        """Test GET /update/<id> for existing todo."""
        # Create a todo first
        with client.application.app_context():
            todo = Todo(content="Original content")
            db.session.add(todo)
            db.session.commit()
            todo_id = todo.id
        
        response = client.get(f'/update/{todo_id}')
        assert response.status_code == 200
        assert b'Original content' in response.data

    @pytest.mark.integration
    def test_update_get_nonexistent_todo(self, client):
        """Test GET /update/<id> for nonexistent todo."""
        response = client.get('/update/9999')
        assert response.status_code == 404

    @pytest.mark.integration
    def test_update_post_existing_todo(self, client):
        """Test POST /update/<id> to update existing todo."""
        # Create a todo first
        with client.application.app_context():
            todo = Todo(content="Original content")
            db.session.add(todo)
            db.session.commit()
            todo_id = todo.id
        
        # Update the todo
        response = client.post(f'/update/{todo_id}',
                             data={'content': 'Updated content'},
                             follow_redirects=True)
        assert response.status_code == 200
        
        # Verify update
        with client.application.app_context():
            updated_todo = Todo.query.get(todo_id)
            assert updated_todo is not None
            assert updated_todo.content == 'Updated content'

    @pytest.mark.integration
    def test_update_post_nonexistent_todo(self, client):
        """Test POST /update/<id> for nonexistent todo."""
        response = client.post('/update/9999',
                             data={'content': 'New content'})
        assert response.status_code == 404

    @pytest.mark.integration
    def test_update_post_empty_content(self, client):
        """Test updating todo with empty content."""
        # Create a todo first
        with client.application.app_context():
            todo = Todo(content="Original content")
            db.session.add(todo)
            db.session.commit()
            todo_id = todo.id
        
        # Update with empty content
        response = client.post(f'/update/{todo_id}',
                             data={'content': ''},
                             follow_redirects=True)
        assert response.status_code == 200
        
        # Verify update
        with client.application.app_context():
            updated_todo = Todo.query.get(todo_id)
            assert updated_todo is not None
            assert updated_todo.content == ''


# Note: Error scenario tests have been removed for simplicity
# They can be added back with proper mocking setup


class TestConcurrentOperations:
    """Tests for concurrent operations and race conditions."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_multiple_simultaneous_creates(self, client):
        """Test creating multiple todos simultaneously."""
        import threading
        import time
        
        results = []
        errors = []
        
        def create_todo(content):
            try:
                response = client.post('/', 
                                     data={'content': content}, 
                                     follow_redirects=True)
                results.append((content, response.status_code))
            except Exception as e:
                errors.append(e)
        
        # Create threads to simulate concurrent requests
        threads = []
        for i in range(10):
            thread = threading.Thread(target=create_todo, args=(f"Concurrent todo {i}",))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 10
        
        # Verify all todos were created
        with client.application.app_context():
            count = Todo.query.filter(Todo.content.like("Concurrent todo%")).count()
            assert count == 10
"""
Performance and load tests for the Flask Todo application.

These tests help identify performance bottlenecks and ensure the app
can handle expected loads.
"""

import pytest
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from flask_todo_app.app import Todo, db


class TestPerformance:
    """Performance tests for the application."""

    @pytest.mark.slow
    def test_create_many_todos_performance(self, client):
        """Test performance when creating many todos."""
        start_time = time.time()
        
        # Create 100 todos
        for i in range(100):
            response = client.post('/', 
                                 data={'content': f'Performance test todo {i}'}, 
                                 follow_redirects=True)
            assert response.status_code == 200
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete within reasonable time (adjust based on your requirements)
        assert duration < 30.0, f"Creating 100 todos took {duration:.2f} seconds"
        
        # Verify all todos were created
        with client.application.app_context():
            count = Todo.query.filter(Todo.content.like("Performance test todo%")).count()
            assert count == 100

    @pytest.mark.slow
    def test_query_performance_with_many_todos(self, client):
        """Test query performance with many todos in database."""
        # First, create many todos
        with client.application.app_context():
            todos = []
            for i in range(500):
                todos.append(Todo(content=f"Query test todo {i}"))
            
            db.session.add_all(todos)
            db.session.commit()
        
        # Now test query performance
        start_time = time.time()
        
        response = client.get('/')
        assert response.status_code == 200
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Query should complete quickly even with many records
        assert duration < 5.0, f"Querying 500+ todos took {duration:.2f} seconds"

    @pytest.mark.slow
    def test_concurrent_operations(self, client):
        """Test concurrent CRUD operations."""
        def create_todo(todo_id):
            response = client.post('/', 
                                 data={'content': f'Concurrent todo {todo_id}'}, 
                                 follow_redirects=True)
            return response.status_code == 200

        def read_todos():
            response = client.get('/')
            return response.status_code == 200

        # Test concurrent creates and reads
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            # Submit create operations
            for i in range(20):
                futures.append(executor.submit(create_todo, i))
            
            # Submit read operations
            for _ in range(10):
                futures.append(executor.submit(read_todos))
            
            # Wait for all operations to complete
            results = [future.result() for future in as_completed(futures)]
        
        # All operations should succeed
        assert all(results), "Some concurrent operations failed"
        
        # Verify creates worked
        with client.application.app_context():
            count = Todo.query.filter(Todo.content.like("Concurrent todo%")).count()
            assert count == 20

    @pytest.mark.slow 
    def test_delete_performance(self, client):
        """Test performance of delete operations."""
        # Create todos to delete
        todo_ids = []
        with client.application.app_context():
            for i in range(50):
                todo = Todo(content=f"Delete test todo {i}")
                db.session.add(todo)
                db.session.commit()
                todo_ids.append(todo.id)
        
        # Measure delete performance
        start_time = time.time()
        
        for todo_id in todo_ids:
            response = client.get(f'/delete/{todo_id}', follow_redirects=True)
            assert response.status_code == 200
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete within reasonable time
        assert duration < 10.0, f"Deleting 50 todos took {duration:.2f} seconds"
        
        # Verify all were deleted
        with client.application.app_context():
            remaining = Todo.query.filter(Todo.content.like("Delete test todo%")).count()
            assert remaining == 0

    @pytest.mark.slow
    def test_update_performance(self, client):
        """Test performance of update operations."""
        # Create todos to update
        todo_ids = []
        with client.application.app_context():
            for i in range(30):
                todo = Todo(content=f"Original content {i}")
                db.session.add(todo)
                db.session.commit()
                todo_ids.append(todo.id)
        
        # Measure update performance
        start_time = time.time()
        
        for i, todo_id in enumerate(todo_ids):
            response = client.post(f'/update/{todo_id}',
                                 data={'content': f'Updated content {i}'},
                                 follow_redirects=True)
            assert response.status_code == 200
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete within reasonable time
        assert duration < 15.0, f"Updating 30 todos took {duration:.2f} seconds"
        
        # Verify updates worked
        with client.application.app_context():
            updated_count = Todo.query.filter(Todo.content.like("Updated content%")).count()
            assert updated_count == 30


class TestMemoryUsage:
    """Tests for memory usage patterns."""

    @pytest.mark.slow
    def test_memory_usage_with_large_dataset(self, client):
        """Test that memory usage stays reasonable with large datasets."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create a large dataset
        with client.application.app_context():
            batch_size = 100
            for batch in range(10):  # 1000 total todos
                todos = []
                for i in range(batch_size):
                    todos.append(Todo(content=f"Memory test todo {batch * batch_size + i}"))
                
                db.session.add_all(todos)
                db.session.commit()
                
                # Clear session to prevent memory accumulation
                db.session.expunge_all()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (adjust threshold as needed)
        assert memory_increase < 100, f"Memory increased by {memory_increase:.2f} MB"
import pytest
import tempfile
import os
from apptest import app, db, Todo


class TestFlaskApp:
    """Test suite for the Flask Todo application"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask application"""
        # Create a temporary file for the test database
        db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                
        # Clean up
        os.close(db_fd)
        os.unlink(app.config['DATABASE'])

    def test_app_is_running(self, client):
        """Test that the application is running and accessible"""
        response = client.get('/')
        assert response.status_code == 200
        print("✓ App is running successfully")

    def test_home_page_loads(self, client):
        """Test that the home page loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
        print("✓ Home page loads correctly")

    def test_metrics_endpoint(self, client):
        """Test that the Prometheus metrics endpoint is accessible"""
        response = client.get('/metrics')
        assert response.status_code == 200
        # Check for some expected Prometheus metrics
        assert b'app_request_count' in response.data or b'python_info' in response.data
        print("✓ Metrics endpoint is accessible")

    def test_add_task_post_request(self, client):
        """Test adding a new task via POST request"""
        response = client.post('/', data={'content': 'Test task'}, follow_redirects=True)
        assert response.status_code == 200
        print("✓ Can add tasks via POST request")

    def test_database_connection(self, client):
        """Test that database operations work"""
        # Create a test task directly in the database
        with app.app_context():
            test_task = Todo(content='Database test task')
            db.session.add(test_task)
            db.session.commit()
            
            # Verify the task was added
            task = Todo.query.filter_by(content='Database test task').first()
            assert task is not None
            assert task.content == 'Database test task'
            print("✓ Database connection and operations work")

    def test_delete_nonexistent_task(self, client):
        """Test deleting a non-existent task returns 404"""
        response = client.get('/delete/9999')
        assert response.status_code == 404
        print("✓ Proper error handling for non-existent tasks")

    def test_update_nonexistent_task(self, client):
        """Test updating a non-existent task returns 404"""
        response = client.get('/update/9999')
        assert response.status_code == 404
        print("✓ Proper error handling for non-existent task updates")

    def test_app_configuration(self, client):
        """Test that the app has correct configuration"""
        assert app.config['TESTING'] is True
        assert 'SQLALCHEMY_DATABASE_URI' in app.config
        print("✓ App configuration is correct")


# Additional simple tests that can be run independently
def test_app_exists():
    """Test that the Flask app object exists"""
    assert app is not None
    print("✓ Flask app object exists")


def test_app_is_flask_instance():
    """Test that app is actually a Flask instance"""
    from flask import Flask
    assert isinstance(app, Flask)
    print("✓ App is a valid Flask instance")


def test_database_model_exists():
    """Test that the Todo model is properly defined"""
    assert Todo is not None
    assert hasattr(Todo, 'id')
    assert hasattr(Todo, 'content')
    assert hasattr(Todo, 'date_created')
    print("✓ Database model is properly defined")


# Main execution for running tests directly
if __name__ == '__main__':
    # Run basic validation tests
    test_app_exists()
    test_app_is_flask_instance()
    test_database_model_exists()
    
    print("\n🎉 Basic app validation completed successfully!")
    print("\nTo run full test suite, use: pytest app_test.py -v")
    print("To run with coverage: pytest app_test.py --cov=apptest -v")
# test_app.py
#import sys
#import os
#from app import app
#def test_home_route():
    # Create a test client using Flask's test client
#    tester = app.test_client()
#    response = tester.get('/')
    # Check if the status code is 200 (OK)
#    assert response.status_code == 200
import os
import tempfile
import pytest
from app import app, db, Todo


@pytest.fixture
def client():
    # Use a temporary file for SQLite DB
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<html' in response.data  # assumes HTML is rendered


def test_index_post(client):
    response = client.post('/', data={'content': 'Test Task'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Task' in response.data  # rendered in HTML


def test_create_and_delete_task(client):
    # Add a task
    client.post('/', data={'content': 'To be deleted'}, follow_redirects=True)
    task = Todo.query.filter_by(content='To be deleted').first()
    assert task is not None

    # Delete the task
    response = client.get(f'/delete/{task.id}', follow_redirects=True)
    assert response.status_code == 200
    deleted = Todo.query.get(task.id)
    assert deleted is None


def test_update_task(client):
    # Add a task
    client.post('/', data={'content': 'Old Task'}, follow_redirects=True)
    task = Todo.query.filter_by(content='Old Task').first()
    assert task is not None

    # Update the task
    response = client.post(f'/update/{task.id}', data={'content': 'Updated Task'}, follow_redirects=True)
    assert response.status_code == 200

    updated_task = Todo.query.get(task.id)
    assert updated_task.content == 'Updated Task'


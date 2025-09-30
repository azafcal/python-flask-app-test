# test_app.py
from app import app

def test_home_route():
    # Create a test client using Flask's test client
    tester = app.test_client()
    response = tester.get('/')
    
    # Check if the status code is 200 (OK)
    assert response.status_code == 200

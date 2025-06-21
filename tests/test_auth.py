import pytest
import sys
import os

# 🧠 Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from extensions import db
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing if you use WTForms
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass'
    }, follow_redirects=True)

    assert b"Registration successful" in response.data
    user = User.query.filter_by(username='testuser').first()
    assert user is not None

def test_login(client):
    client.post('/register', data={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'pass123'
    }, follow_redirects=True)

    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'pass123'
    }, follow_redirects=True)

    assert b"Dashboard" in response.data or b"Welcome" in response.data

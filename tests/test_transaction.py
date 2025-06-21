import pytest
from app import app, db
from models import User, Transaction
from flask_login import login_user
from flask import session

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def register_and_login(client):
    # Register
    client.post('/register', data={
        'username': 'transuser',
        'email': 'trans@example.com',
        'password': 'test123'
    }, follow_redirects=True)

    # Login
    client.post('/login', data={
        'username': 'transuser',
        'password': 'test123'
    }, follow_redirects=True)

def test_add_transaction(client):
    with app.app_context():
        register_and_login(client)
        response = client.post('/add', data={
            'type': 'income',
            'category': 'Salary',
            'amount': '5000'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Transaction added' in response.data

        transaction = Transaction.query.first()
        assert transaction is not None
        assert transaction.category == 'Salary'
        assert transaction.amount == 5000

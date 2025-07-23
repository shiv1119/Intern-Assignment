import pytest
import sqlite3
import bcrypt
from app import create_app  # assuming you have a create_app() factory
from flask import g

@pytest.fixture
def client():
    app = create_app(testing=True)

    with app.test_client() as client:
        with app.app_context():
            db = app.db
            db.execute("DROP TABLE IF EXISTS users")
            db.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            """)
            db.commit()
        yield client

# This test verifies that user with valid email and valid passwords gets a new account on our server
def test_create_user(client):
    response = client.post('/users', json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "StrongPass1!"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User created successfully"

# This test ensures that when a user tries to create an account with an email that already exists raises a 409 request. 
def test_duplicate_email(client):
    client.post('/users', json={
        "name": "Bob",
        "email": "bob@example.com",
        "password": "StrongPass2!"
    })
    response = client.post('/users', json={
        "name": "Bob 2",
        "email": "bob@example.com",
        "password": "StrongPass3!"
    })
    assert response.status_code == 409
    assert "already exists" in response.get_json()["error"]

# Ensures user creation fails when password is week and does not meet our expectation
def test_weak_password(client):
    response = client.post('/users', json={
        "name": "WeakUser",
        "email": "weak@example.com",
        "password": "123"
    })
    assert response.status_code == 400
    assert "strong password" in response.get_json()["error"].lower()

# This test checks for getting all user
def test_get_all_users(client):
    client.post('/users', json={
        "name": "Test",
        "email": "test@example.com",
        "password": "StrongPass1!"
    })
    response = client.get('/users')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# This test tests out get user by id route after creation
def test_get_user_by_id(client):
    post_resp = client.post('/users', json={
        "name": "Charlie",
        "email": "charlie@example.com",
        "password": "StrongPass4!"
    })
    assert post_resp.status_code == 201
    user_id = 1
    response = client.get(f'/user/{user_id}')
    assert response.status_code == 200
    assert response.get_json()['email'] == 'charlie@example.com'

# tests update functionalities 
def test_update_user(client):
    client.post('/users', json={
        "name": "Dave",
        "email": "dave@example.com",
        "password": "StrongPass5!"
    })
    response = client.put('/user/1', json={
        "name": "Dave Updated",
        "email": "daveupdated@example.com"
    })
    assert response.status_code == 200
    assert "updated" in response.get_json()["message"].lower()

# Tests delete route and ensures if user exists then it can be deleted by id
def test_delete_user(client):
    client.post('/users', json={
        "name": "Eve",
        "email": "eve@example.com",
        "password": "StrongPass6!"
    })
    response = client.delete('/user/1')
    assert response.status_code == 200
    assert "deleted" in response.get_json()["message"].lower()

# This test ensures that we can find a user by partial name match
def test_search_user(client):
    client.post('/users', json={
        "name": "Frank",
        "email": "frank@example.com",
        "password": "StrongPass7!"
    })
    response = client.get('/search?name=Fran')
    assert response.status_code == 200
    assert len(response.get_json()) > 0

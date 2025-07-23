import pytest
import bcrypt
import sqlite3
from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.db.connection import get_db


@pytest.fixture
def client():
    app = Flask(__name__)
    app.db = get_db()

    with app.app_context():
        cursor = app.db.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        app.db.commit()

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    with app.test_client() as client:
        yield client


def test_login_success(client):
    password = "Test@1234"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                   ("John Doe", "john@example.com", hashed_password))
    conn.commit()

    response = client.post('/login', json={
        "email": "john@example.com",
        "password": "Test@1234"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "user_id" in data


def test_login_wrong_password(client):
    password = "Correct@123"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                   ("Jane Smith", "jane@example.com", hashed_password))
    conn.commit()

    response = client.post('/login', json={
        "email": "jane@example.com",
        "password": "WrongPassword"
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data["status"] == "failed"


def test_login_user_not_found(client):
    response = client.post('/login', json={
        "email": "no_user@example.com",
        "password": "irrelevant"
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data["status"] == "failed"

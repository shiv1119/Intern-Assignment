from flask import Blueprint, request, jsonify, current_app
from app.utils.errors import database_error, exception_error
from app.utils.password_checker import is_strong_password
import sqlite3
import bcrypt

import json

user_bp = Blueprint('user_bp', __name__)

# Returns a welcome message confirming the User Management System is running
@user_bp.route('/')
def home():
    return "User Management System", 200

#Get all user - fetches all the users  in pagination form to increase throughput of the api
@user_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))

        conn = current_app.db
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, email FROM users LIMIT ? OFFSET ?", (limit, offset))
        rows = cursor.fetchall()

        if not rows:
            return jsonify({"message": "No users found"}), 200

        users = [dict(row) for row in rows]
        return jsonify(users), 200

    except ValueError:
        return jsonify({"error": "Invalid limit or offset. Must be integers"}), 400
    except sqlite3.Error as e:
        return database_error(e)
    except Exception as e:
        return exception_error(e)

# Get user by id - This route returns user information by taking id
@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = current_app.db
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "User not found"}), 404

        return jsonify(dict(row)), 200

    except sqlite3.Error as e:
        return database_error(e)
    except Exception as e:
        return exception_error(e)

# Create User - Creates a new user after validating password strength and ensuring the email is unique.
@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        raw_password = data['password']

        is_strong, msg = is_strong_password(raw_password)
        if not is_strong:
            return jsonify({"error": msg}), 400

        conn = current_app.db
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return jsonify({"error": "User with this email already exists. Try login"}), 409

        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                       (name, email, hashed_password))
        conn.commit()

        return jsonify({"message": "User created successfully"}), 201

    except sqlite3.Error as e:
        return database_error(e)
    except Exception as e:
        return exception_error(e)

# Update User - Updates a user’s name and email by ID, with validation.
@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Invalid input"}), 400

        conn = current_app.db
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User updated successfully"}), 200

    except sqlite3.Error as e:
        return database_error(e)
    except Exception as e:
        return exception_error(e)

# Delete User - Deletes a user by id
@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = current_app.db
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": f"User deleted Successfully."}), 200

    except sqlite3.Error as e:
        return database_error(e)
    except Exception as e:
        return exception_error(e)

# Search By Name- Searches users by partial or full name using the name query parameter.
@user_bp.route('/search', methods=['GET'])
def search_users():
    try:
        name = request.args.get('name')
        if not name:
            return jsonify({"error": "Please provide a name to search"}), 400

        conn = current_app.db
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", ('%' + name + '%',))
        rows = cursor.fetchall()

        if not rows:
            return jsonify({"message": "No users found"}), 200

        return jsonify([dict(row) for row in rows]), 200

    except sqlite3.Error as e:
        return database_error(e)
    except Exception as e:
        return exception_error(e)

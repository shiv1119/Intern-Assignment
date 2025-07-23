from flask import Blueprint, request, jsonify, current_app
import bcrypt
import sqlite3

auth_bp = Blueprint('auth_bp', __name__)

# Login  - User can login by giving their email and password if account exists
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password'].encode('utf-8') 

        conn = current_app.db
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password, user[1]):
            return jsonify({"status": "success", "message":"User logged in successfully", "user_id": user[0]}), 200
        else:
            return jsonify({"status": "failed", "message": "Invalid credentials"}), 401

    except sqlite3.Error as e:
        return jsonify({"status": "error", "message": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": "Internal error", "details": str(e)}), 500

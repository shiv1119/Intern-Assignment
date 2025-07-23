from flask import jsonify


# Reusable function to handel the database and server error. To follow DRY principle
def database_error(e):
    return jsonify({"error": "Database error", "details": str(e)}), 500

# Reusable function to handel generic exceptions
def exception_error(e):
    return jsonify({"error": "Internal server error", "details": str(e)}), 500

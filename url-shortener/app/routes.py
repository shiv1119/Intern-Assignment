from flask import Blueprint, request, jsonify, redirect
from app.storage import store
from app.utils import generate_short_code, is_valid_url
from datetime import datetime, UTC

bp = Blueprint('url_shortener', __name__)

# This route will create a short code for a valid long url and stores in storage. It also returns shortened url with short code
@bp.route("/api/shorten", methods=["POST"])
def shorten_url():
    try:
        data = request.get_json()
        long_url = data.get("url")

        if not long_url or not is_valid_url(long_url):
            return jsonify({"error": "Invalid or missing URL"}), 400

        short_code = generate_short_code()
        store[short_code] = {
            "url": long_url,
            "clicks": 0,
            "created_at": datetime.now(UTC).isoformat()
        }

        return jsonify({
            "short_code": short_code,
            "short_url": f"http://localhost:5000/{short_code}"
        }), 201

    except Exception as e:
        return jsonify({"error": "Something went wrong while shortening URL", "details": str(e)}), 500


# This route redirects the user to the original url using generated short code
@bp.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    try:
        data = store.get(short_code)
        if not data:
            return jsonify({"error": "Short code not found"}), 404

        data["clicks"] += 1
        return redirect(data["url"])

    except Exception as e:
        return jsonify({"error": "Something went wrong during redirection", "details": str(e)}), 500

# Returns analytics as instructed in assignment  (Original URL,Total click count, creation time)
@bp.route("/api/stats/<short_code>", methods=["GET"])
def get_stats(short_code):
    try:
        data = store.get(short_code)
        if not data:
            return jsonify({"error": "Short code not found"}), 404

        return jsonify({
            "url": data["url"],
            "clicks": data["clicks"],
            "created_at": data["created_at"]
        })

    except Exception as e:
        return jsonify({"error": "Something went wrong while fetching stats", "details": str(e)}), 500

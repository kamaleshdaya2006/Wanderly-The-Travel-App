from flask import Blueprint, jsonify
from db import get_connection

hidden_gems_bp = Blueprint("hidden_gems", __name__)

# ---------------------------------
# Get hidden gem places
# ---------------------------------
@hidden_gems_bp.route("/hidden-gems", methods=["GET"])
def get_hidden_gems():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT place_id, name, description, image, category
            FROM places
            WHERE LOWER(category) = 'hidden'
        """)

        places = []
        for row in cursor:
            places.append({
                "place_id": row[0],
                "name": row[1],
                "description": row[2] if row[2] else "",
                "image": row[3],
                "category": row[4]
            })

        return jsonify(places)

    finally:
        cursor.close()
        conn.close()

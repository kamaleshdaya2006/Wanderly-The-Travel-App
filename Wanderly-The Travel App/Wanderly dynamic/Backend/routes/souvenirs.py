from flask import Blueprint, jsonify, request
from db import get_connection

souvenirs_bp = Blueprint("souvenirs", __name__)


# ----------------------------------------------------
# GET ALL SOUVENIRS
# ----------------------------------------------------
@souvenirs_bp.route("/souvenirs", methods=["GET"])
def get_all_souvenirs():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT s.souvenir_id,
                   s.place_id,
                   s.name,
                   s.description,
                   s.rating,
                   s.shop_name,
                   p.name
            FROM souvenirs s
            JOIN places p ON s.place_id = p.place_id
            WHERE p.status = 'approved'
            ORDER BY s.rating DESC NULLS LAST
        """)

        souvenirs = []
        for row in cursor:
            souvenirs.append({
                "souvenir_id": row[0],
                "place_id": row[1],
                "name": row[2],
                "description": row[3] if row[3] else "",
                "rating": float(row[4]) if row[4] else None,
                "shop_name": row[5],
                "place_name": row[6]
            })

        return jsonify(souvenirs)

    finally:
        cursor.close()
        conn.close()


# ----------------------------------------------------
# ADD SOUVENIR
# ----------------------------------------------------
@souvenirs_bp.route("/souvenirs", methods=["POST"])
def add_souvenir():
    data = request.json

    required = ["place_id", "name", "description"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    normalized_name = data["name"].strip().lower()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Validate place exists
        cursor.execute("SELECT 1 FROM places WHERE place_id = %s",
                       [data["place_id"]])

        if not cursor.fetchone():
            return jsonify({"error": "Invalid place_id"}), 400

        # Duplicate souvenir per place
        cursor.execute("""
            SELECT COUNT(*)
            FROM souvenirs
            WHERE place_id = %s
            AND LOWER(TRIM(name)) = %s
        """, [data["place_id"], normalized_name])

        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "Souvenir already exists for this place"}), 409

        cursor.execute("""
            INSERT INTO souvenirs
            (place_id, name, description, rating, shop_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            int(data["place_id"]),
            data["name"].strip(),
            data["description"],
            float(data["rating"]) if data.get("rating") else None,
            data.get("shop_name")
        ))

        conn.commit()
        return jsonify({"message": "Souvenir added successfully"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
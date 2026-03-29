from flask import Blueprint, jsonify, request
from db import get_connection

foods_bp = Blueprint("foods", __name__)


# ----------------------------------------------------
# GET ALL FOODS
# ----------------------------------------------------
@foods_bp.route("/foods", methods=["GET"])
def get_all_foods():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT f.food_id,
                   f.name,
                   f.description,
                   f.rating,
                   f.shop_name,
                   p.place_id,
                   p.name
            FROM foods f
            JOIN places p ON f.place_id = p.place_id
            WHERE p.status = 'approved'
            ORDER BY f.rating DESC NULLS LAST
        """)

        foods = []
        for row in cursor:
            foods.append({
                "food_id": row[0],
                "name": row[1],
                "description": row[2] if row[2] else "",
                "rating": float(row[3]) if row[3] else None,
                "shop_name": row[4],
                "place_id": row[5],
                "place_name": row[6]
            })

        return jsonify(foods)

    finally:
        cursor.close()
        conn.close()


# ----------------------------------------------------
# ADD FOOD
# ----------------------------------------------------
@foods_bp.route("/foods", methods=["POST"])
def add_food():
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

        # Duplicate food per place
        cursor.execute("""
            SELECT COUNT(*)
            FROM foods
            WHERE place_id = %s
            AND LOWER(TRIM(name)) = %s
        """, [data["place_id"], normalized_name])

        if cursor.fetchone()[0] > 0:
            return jsonify({"error": "Food already exists for this place"}), 409

        cursor.execute("""
            INSERT INTO foods
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
        return jsonify({"message": "Food added successfully"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
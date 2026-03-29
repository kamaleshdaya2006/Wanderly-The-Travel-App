from flask import Blueprint, jsonify, request
from db import get_connection

places_bp = Blueprint("places", __name__)


# ----------------------------------------------------
# GET ALL PLACES OR BY CATEGORY
# ----------------------------------------------------
@places_bp.route("/places", methods=["GET"])
def get_places():

    category = request.args.get("category")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if category:
            cursor.execute("""
                SELECT place_id, name, description, image, category
                FROM places
                WHERE LOWER(category) = LOWER(%s)
            """, [category])
        else:
            cursor.execute("""
                SELECT place_id, name, description, image, category
                FROM places
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


# ----------------------------------------------------
# GET SINGLE PLACE WITH RELATED DATA
# ----------------------------------------------------
@places_bp.route("/places/<int:place_id>", methods=["GET"])
def get_place(place_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Place Info
        cursor.execute("""
            SELECT place_id, name, description, image, category
            FROM places
            WHERE place_id = %s
        """, [place_id])

        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Place not found"}), 404

        place_data = {
            "place_id": row[0],
            "name": row[1],
            "description": row[2] if row[2] else "",
            "image": row[3],
            "category": row[4]
        }

        # 2️⃣ Foods
        cursor.execute("""
            SELECT food_id, name, description, rating, shop_name
            FROM foods
            WHERE place_id = %s
        """, [place_id])

        foods = []
        for f in cursor:
            foods.append({
                "food_id": f[0],
                "name": f[1],
                "description": f[2] if f[2] else "",
                "rating": float(f[3]) if f[3] else None,
                "shop_name": f[4]
            })

        # 3️⃣ Souvenirs
        cursor.execute("""
            SELECT souvenir_id, name, description, rating, shop_name
            FROM souvenirs
            WHERE place_id = %s
        """, [place_id])

        souvenirs = []
        for s in cursor:
            souvenirs.append({
                "souvenir_id": s[0],
                "name": s[1],
                "description": s[2] if s[2] else "",
                "rating": float(s[3]) if s[3] else None,
                "shop_name": s[4]
            })

        # 4️⃣ Activities
        cursor.execute("""
            SELECT activity_id, name, description, icon
            FROM activities
            WHERE place_id = %s
        """, [place_id])

        activities = []
        for a in cursor:
            activities.append({
                "activity_id": a[0],
                "name": a[1],
                "description": a[2] if a[2] else "",
                "icon": a[3]
            })

        # 5️⃣ Reviews
        cursor.execute("""
            SELECT review_id, rating, review_text, created_at
            FROM reviews
            WHERE place_id = %s
            ORDER BY created_at DESC
        """, [place_id])

        reviews = []
        for r in cursor:
            reviews.append({
                "review_id": r[0],
                "rating": r[1],
                "text": r[2] if r[2] else "",
                "created_at": str(r[3])
            })

        return jsonify({
            "place": place_data,
            "foods": foods,
            "souvenirs": souvenirs,
            "activities": activities,
            "reviews": reviews
        })

    finally:
        cursor.close()
        conn.close()
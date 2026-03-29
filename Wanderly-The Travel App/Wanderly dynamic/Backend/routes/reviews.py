from flask import Blueprint, request, jsonify
from db import get_connection

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.route("/reviews", methods=["POST"])
def add_review():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        data = request.get_json()

        user_id = data.get("user_id")
        entity_type = data.get("entity_type")
        entity_id = data.get("entity_id")
        rating = data.get("rating")
        review_text = data.get("review_text")

        # validation
        if not user_id or not entity_type or not entity_id or not review_text:
            return jsonify({"error": "Missing fields"}), 400

        cursor.execute("""
            INSERT INTO reviews
            (place_id, user_id, rating, review_text, created_at,
             entity_type, entity_id)
            VALUES
            (NULL,
             %(user_id)s,
             %(rating)s,
             %(review_text)s,
             NOW(),
             %(entity_type)s,
             %(entity_id)s)
        """, {
            "user_id": user_id,
            "rating": rating,
            "review_text": review_text,
            "entity_type": entity_type,
            "entity_id": entity_id
        })

        conn.commit()
        return jsonify({"message": "Review added successfully"})

    except Exception as e:
        print("REVIEW ERROR:", e)
        if conn:
            conn.rollback()
        return jsonify({"error": "Failed"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@reviews_bp.route("/reviews", methods=["GET"])
def get_reviews():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        entity_type = request.args.get("entity_type")
        entity_id = request.args.get("entity_id")

        if not entity_type or not entity_id:
            return jsonify({"error": "Missing parameters"}), 400

        cursor.execute("""
            SELECT review_id, user_id, rating, review_text, created_at
            FROM reviews
            WHERE entity_type = %s AND entity_id = %s
            ORDER BY created_at DESC
        """, [entity_type, entity_id])

        reviews = []
        for row in cursor:
            reviews.append({
                "review_id": row[0],
                "user_id": row[1],
                "rating": row[2],
                "review_text": row[3] if row[3] else "",
                "created_at": str(row[4])
            })

        return jsonify(reviews)

    except Exception as e:
        print("GET REVIEWS ERROR:", e)
        return jsonify({"error": "Failed"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
from flask import Blueprint, jsonify, request
from db import get_connection
import os
from werkzeug.utils import secure_filename
import uuid

guides_bp = Blueprint("guides", __name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ================= GET GUIDES =================
@guides_bp.route("/guides", methods=["GET"])
def get_guides():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT guide_id, name, description, languages,
                   rating, price_per_day, image
            FROM guides
        """)

        guides = []

        for row in cursor:
            guides.append({
                "guide_id": row[0],
                "name": row[1],
                "description": row[2] if row[2] else "",
                "languages": row[3],
                "rating": row[4],
                "price": row[5],
                "image": row[6]
            })

        return jsonify(guides)

    finally:
        cursor.close()
        conn.close()


# ================= ADD GUIDE =================
@guides_bp.route("/guides", methods=["POST"])
def add_guide():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        name = request.form.get("name")
        desc = request.form.get("description")
        lang = request.form.get("languages")
        price = request.form.get("price")
        user_id = request.form.get("user_id")

        file = request.files.get("image")
        filename = None

        if file and file.filename != "":
            unique_name = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(filepath)
            filename = unique_name

        cursor.execute("""
            INSERT INTO guides
            (name, description, languages,
             price_per_day, user_id, image, status)
            VALUES
            (%(name)s, %(description)s, %(languages)s,
             %(price)s, %(user_id)s, %(image)s, 'pending')
        """, {
            "name": name,
            "description": desc,
            "languages": lang,
            "price": price,
            "user_id": user_id,
            "image": filename
        })

        conn.commit()
        return jsonify({"message": "Guide added"})

    finally:
        cursor.close()
        conn.close()


# ================= BOOK GUIDE =================
@guides_bp.route("/guide-bookings", methods=["POST"])
def create_booking():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        data = request.get_json()

        user_id = data["user_id"]
        guide_id = data["guide_id"]
        booking_date = data["booking_date"]

        cursor.execute("""
            INSERT INTO guide_bookings
            (user_id, guide_id, trip_id,
             booking_date, status)
            VALUES
            (%(user_id)s, %(guide_id)s,
             NULL, %(booking_date)s::date, 'confirmed')
        """, {
            "user_id": user_id,
            "guide_id": guide_id,
            "booking_date": booking_date
        })

        conn.commit()
        return jsonify({"message": "Booking successful"})

    finally:
        cursor.close()
        conn.close()
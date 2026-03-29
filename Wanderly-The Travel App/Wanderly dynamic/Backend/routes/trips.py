from flask import Blueprint, jsonify, request
from db import get_connection

trips_bp = Blueprint("trips", __name__)

# -----------------------------
# Get trips of a user
# -----------------------------
@trips_bp.route("/trips/<int:user_id>", methods=["GET"])
def get_trips(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT trip_id, trip_name, days, created_at
            FROM trips
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, [user_id])

        trips = []
        for t in cursor:
            trips.append({
                "trip_id": t[0],
                "name": t[1],
                "days": t[2],
                "created_at": str(t[3])
            })

        return jsonify(trips)

    finally:
        cursor.close()
        conn.close()


# -----------------------------
# Create new trip
# -----------------------------
@trips_bp.route("/trips", methods=["POST"])
def create_trip():
    data = request.json
    user_id = data["user_id"]
    name = data["name"]
    days = data["days"]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO trips (user_id, trip_name, days)
            VALUES (%s, %s, %s)
            RETURNING trip_id
        """, [user_id, name, days])

        conn.commit()
        return jsonify({"message": "Trip created"})

    finally:
        cursor.close()
        conn.close()


# -----------------------------
# Delete trip
# -----------------------------
@trips_bp.route("/trips/<int:trip_id>", methods=["DELETE"])
def delete_trip(trip_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Delete child rows first
        cursor.execute("""
            DELETE FROM trip_places
            WHERE trip_id = %s
        """, [trip_id])

        # 2️⃣ Then delete parent row
        cursor.execute("""
            DELETE FROM trips
            WHERE trip_id = %s
        """, [trip_id])

        conn.commit()
        return jsonify({"message": "Trip deleted successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# -----------------------------
# Add place to trip
# -----------------------------
@trips_bp.route("/trip_places", methods=["POST"])
def add_place_to_trip():
    data = request.json
    trip_id = data["trip_id"]
    place_id = data["place_id"]
    day_number = data["day_number"]
    order_in_day = data["order_in_day"]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO trip_places (trip_id, place_id, day_number, order_in_day)
            VALUES (%s, %s, %s, %s)
        """, [trip_id, place_id, day_number, order_in_day])

        conn.commit()
        return jsonify({"message": "Place added to trip"})

    finally:
        cursor.close()
        conn.close()

@trips_bp.route("/search_places")
def search_places():
    query = request.args.get("q", "").lower()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT place_id, name, description, image
            FROM places
            WHERE LOWER(name) LIKE %s
            LIMIT 10
        """, [f"%{query}%"])

        results = []
        for row in cursor:
            desc = row[2] if row[2] else ""
            results.append({
                "place_id": row[0],
                "name": row[1],
                "description": desc[:120],
                "image": row[3]
            })

        return jsonify(results)

    finally:
        cursor.close()
        conn.close()

@trips_bp.route("/trip_places/<int:trip_id>")
def get_trip_places(trip_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT tp.id, tp.day_number, p.name
            FROM trip_places tp
            JOIN places p ON p.place_id = tp.place_id
            WHERE tp.trip_id = %s
            ORDER BY tp.day_number, tp.order_in_day
        """, [trip_id])

        days = {}

        for row in cursor:
            day = str(row[1])   # convert to string for JSON key
            if day not in days:
                days[day] = []
            days[day].append({
                "id": row[0],
                "name": row[2]
            })

        return jsonify(days)

    finally:
        cursor.close()
        conn.close()

@trips_bp.route("/trip_places/<int:tp_id>", methods=["DELETE"])
def remove_place(tp_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM trip_places
            WHERE id = %s
        """, [tp_id])

        conn.commit()
        return jsonify({"message": "Place removed"})

    finally:
        cursor.close()
        conn.close()

@trips_bp.route("/trip_places/<int:tp_id>", methods=["PUT"])
def move_place(tp_id):
    data = request.json
    new_day = data["day_number"]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE trip_places
            SET day_number = %s
            WHERE id = %s
        """, [new_day, tp_id])

        conn.commit()
        return jsonify({"message": "Place moved"})

    finally:
        cursor.close()
        conn.close()

@trips_bp.route("/trips/<int:trip_id>", methods=["PUT"])
def update_trip(trip_id):
    data = request.json
    days = data["days"]
    start_date = data["start_date"]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE trips
            SET days = %s,
                start_date = %s::date
            WHERE trip_id = %s
        """, [days, start_date, trip_id])

        conn.commit()
        return jsonify({"message": "Trip updated"})

    finally:
        cursor.close()
        conn.close()

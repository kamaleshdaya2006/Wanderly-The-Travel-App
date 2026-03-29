from flask import Blueprint, request, jsonify
from db import get_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT user_id, name, email, password, city
            FROM users
            WHERE email = %(email)s
        """, {"email": email})

        user = cursor.fetchone()

        if not user:
            return jsonify({"message": "User not found"}), 401

        db_password = user[3]

        if password != db_password:
            return jsonify({"message": "Invalid password"}), 401

        result = {
            "message": "Login successful",
            "user_id": user[0],
            "name": user[1],
            "email": user[2],
            "city": user[4]
        }

        return jsonify(result)

    finally:
        cursor.close()
        conn.close()

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    city = data.get("city")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check if email already exists
        cursor.execute(
            "SELECT user_id FROM users WHERE email = %(email)s",
            {"email": email}
        )

        if cursor.fetchone():
            return jsonify({"message": "Email already registered"}), 400

        # Insert new user
        cursor.execute("""
            INSERT INTO users (name, email, password, city)
            VALUES (%(name)s, %(email)s, %(password)s, %(city)s)
        """, {
            "name": name,
            "email": email,
            "password": password,
            "city": city
        })

        conn.commit()
        return jsonify({"message": "Signup successful"})

    finally:
        cursor.close()
        conn.close()

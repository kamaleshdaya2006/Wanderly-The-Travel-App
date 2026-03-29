from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.places import places_bp
from routes.auth import auth_bp
from routes.guides import guides_bp
from routes.foods import foods_bp
from routes.souvenirs import souvenirs_bp
from routes.hiddengems import hidden_gems_bp
from routes.trips import trips_bp
from routes.reviews import reviews_bp

app = Flask(__name__)

# Allow both the production Vercel frontend and local dev origins.
# supports_credentials=True lets cookies/auth headers through if needed.
CORS(
    app,
    origins=[
        "https://wanderly-project.vercel.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    supports_credentials=True,
)

app.register_blueprint(souvenirs_bp)
app.register_blueprint(places_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(guides_bp)
app.register_blueprint(foods_bp)
app.register_blueprint(hidden_gems_bp)
app.register_blueprint(trips_bp)
app.register_blueprint(reviews_bp)

@app.route('/static_files/<path:filename>')
def static_files(filename):
    return send_from_directory('../../Wanderly_static', filename)

if __name__ == "__main__":
    app.run(debug=True)
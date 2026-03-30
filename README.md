🌍 Wanderly – Smart Travel Platform

Wanderly is a full-stack tourism web application designed to help users explore destinations, guides, food spots, and hidden gems efficiently. It combines a static frontend with a Python-based backend to deliver structured, dynamic travel data.

🚀 Features
🗺️ Explore places, guides, food, and hidden gems
🧭 Structured travel discovery with categorized content
🔐 Authentication system (login/signup support)
⭐ Reviews and trip management system
🧳 Souvenirs and travel planning modules
⚡ Fast static frontend with dynamic backend APIs
🏗️ Tech Stack

Frontend

HTML, CSS, JavaScript

Backend

Python (Flask)

Database

SQLite / (your DB in db.py)
📂 Project Structure
Wanderly-The Travel App/
│
├── Wanderly_static/        # Frontend (UI)
│   ├── signin.html
│   ├── homepage.css
│   ├── guides.html / .css / .js
│   ├── hidden-gems.html / .css
│   ├── images (Chennai, places, etc.)
│   └── other static assets
│
├── Wanderly dynamic/
│   └── Backend/
│       ├── app.py          # Main Flask app
│       ├── db.py           # Database logic
│       ├── routes/
│       │   ├── auth.py
│       │   ├── places.py
│       │   ├── guides.py
│       │   ├── foods.py
│       │   ├── hiddengems.py
│       │   ├── reviews.py
│       │   ├── souvenirs.py
│       │   └── trips.py
│       ├── static/
│       ├── requirements.txt
│       └── Procfile
│
└── .gitignore
⚙️ Setup & Installation
1. Clone the repo
git clone https://github.com/your-username/wanderly.git
cd wanderly
2. Setup backend
cd "Wanderly dynamic/Backend"

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
3. Run server
python app.py

Server runs at:

http://127.0.0.1:5000
🌐 Running Frontend

Open directly:

Wanderly_static/signin.html

🔌 API Modules (Backend)
/auth → User authentication
/places → Tourist places
/guides → Travel guides
/foods → Food locations
/hiddengems → Hidden spots
/reviews → User reviews
/souvenirs → Shopping items
/trips → Trip planning

The Website is also publicly hosted :
Link for the website : https://wanderly-project.vercel.app/Signin.html

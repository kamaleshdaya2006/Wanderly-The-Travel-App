import psycopg2
import os

# Use DATABASE_URL from env (set on Render) with a fallback to the local
# Supabase connection string for development.
LOCAL_DB_URL = "postgresql://postgres:postgres@localhost:5432/wanderly"

def get_connection():
    db_url = os.environ.get("DATABASE_URL", LOCAL_DB_URL)
    connection = psycopg2.connect(db_url)
    return connection
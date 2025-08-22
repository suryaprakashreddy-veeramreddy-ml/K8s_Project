from flask import Flask, request, jsonify
from flask_cors import CORS  # add this
import psycopg2
import os

 # enable CORS for all routes

from dotenv import load_dotenv
load_dotenv()  # This will load variables from .env file

app = Flask(__name__)
CORS(app) 

# Get DB config from env variables
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5433")
DB_NAME = os.environ.get("DB_NAME", "persondb")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

# Connect to Postgres
conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
    user=DB_USER, password=DB_PASSWORD
)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS person (
    id SERIAL PRIMARY KEY,
    name TEXT,
    age INT,
    phone TEXT
)
""")
conn.commit()

@app.route("/persons", methods=["GET"])
def get_persons():
    cur.execute("SELECT id, name, age, phone FROM person")
    rows = cur.fetchall()
    data = [{"id": r[0], "name": r[1], "age": r[2], "phone": r[3]} for r in rows]
    return jsonify(data)

@app.route("/persons", methods=["POST"])
def add_person():
    data = request.json
    cur.execute(
        "INSERT INTO person (name, age, phone) VALUES (%s, %s, %s)",
        (data["name"], data["age"], data["phone"])
    )
    conn.commit()
    return jsonify({"status": "success"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import uuid
import json

app = Flask(__name__)
CORS(app)

def db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn
    
@app.route("/")
def home():
    return jsonify({"status": "Server is running", "message": "API Task Management is ready!"})

@app.route("/api/share", methods=["POST"])
def create_share():

    data = request.json
    share_id = str(uuid.uuid4())[:8]

    conn = db()

    conn.execute(
        "INSERT INTO shares(id,data) VALUES (?,?)",
        (share_id, json.dumps(data))
    )

    conn.commit()

    return jsonify({"id": share_id})

@app.route("/api/share/<id>")
def get_share(id):

    conn = db()

    row = conn.execute(
        "SELECT data FROM shares WHERE id=?",
        (id,)
    ).fetchone()

    if not row:
        return jsonify({"error":"not found"}),404

    return jsonify(json.loads(row["data"]))


if __name__ == "__main__":

    conn = db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS shares(
        id TEXT PRIMARY KEY,
        data TEXT
    )
    """)

    conn.commit()

    app.run()


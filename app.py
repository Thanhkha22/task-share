from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import uuid
import json

app = Flask(__name__)
# Cho phép GitHub Pages truy cập vào API này
CORS(app)

def db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

# KHỞI TẠO BẢNG: Phải đưa ra ngoài để Gunicorn thực thi ngay khi load app
with db() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS shares(
        id TEXT PRIMARY KEY,
        data TEXT
    )
    """)
    conn.commit()

# Thêm route trang chủ để không bị lỗi "Not Found" khi kiểm tra URL
@app.route("/")
def home():
    return jsonify({"status": "Server is running", "message": "API Task Share ready"})

@app.route("/api/share", methods=["POST"])
def create_share():
    try:
        data = request.json
        share_id = str(uuid.uuid4())[:8]
        with db() as conn:
            conn.execute(
                "INSERT INTO shares(id,data) VALUES (?,?)",
                (share_id, json.dumps(data))
            )
            conn.commit()
        return jsonify({"id": share_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/share/<id>")
def get_share(id):
    with db() as conn:
        row = conn.execute(
            "SELECT data FROM shares WHERE id=?",
            (id,)
        ).fetchone()
    if not row:
        return jsonify({"error":"not found"}), 404
    return jsonify(json.loads(row["data"]))

if __name__ == "__main__":
    app.run()

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/share", methods=["POST"])
def share():

    data = request.json

    return jsonify({
        "status":"ok"
    })

if __name__ == "__main__":
    app.run()
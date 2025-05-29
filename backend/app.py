import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
from db import users
from model.story_gen import generate_story  # ✅ Make sure story_gen.py exists

app = Flask(__name__)
CORS(app)  # Allow all origins for dev

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route("/generate-story", methods=["POST"])
def generate():
    data = request.json
    keywords = data.get("keywords", [])
    email = data.get("email")
    if not keywords or not email:
        return jsonify({"error": "Missing keywords or email"}), 400

    story = generate_story(keywords)

    users.update_one(
        {"email": email},
        {"$push": {
            "history": {
                "keywords": keywords,
                "story": story,
                "timestamp": datetime.datetime.now(datetime.timezone.utc)
            }
        }},
        upsert=True
    )

    return jsonify({"story": story})

@app.route("/get-history", methods=["POST"])
def get_history():
    data = request.json
    email = data.get("email")
    if not email:
        return jsonify({"error": "Missing email"}), 400

    user = users.find_one({"email": email})
    if not user or "history" not in user:
        return jsonify({"history": []})

    return jsonify({"history": user["history"]})

if __name__ == "__main__":
    app.run(debug=True)

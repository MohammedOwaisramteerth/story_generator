from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["story_app"]
users = db["users"]  # ✅ This is what app.py is trying to import

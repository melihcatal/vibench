from pymongo import MongoClient

MONGODB_ATLAS_URI = "your-mongodb-atlas-uri"

client = MongoClient(MONGODB_ATLAS_URI)
db = client.onboarding


def store_profile_note(user_id, note):
    db.notes.insert_one({"user_id": user_id, "note": note})

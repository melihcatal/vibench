import os
from pymongo import MongoClient

# Set up the MongoDB client
client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
db = client["onboarding"]
collection = db["notes"]


def store_profile_note(user_id, note):
    try:
        collection.insert_one({"user_id": user_id, "note": note})
        return True
    except Exception as e:
        print(e)
        return False

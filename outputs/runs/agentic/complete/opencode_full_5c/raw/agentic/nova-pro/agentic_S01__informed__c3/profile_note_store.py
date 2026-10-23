from pymongo import MongoClient


def store_profile_note(note):
    client = MongoClient("YOUR_MONGODB_ATLAS_URI")
    db = client["onboarding"]
    collection = db["notes"]
    collection.insert_one({"note": note})

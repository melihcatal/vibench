import os
from pymongo import MongoClient


def store_profile_note(note):
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
    db = client["onboarding"]
    collection = db["notes"]
    collection.insert_one({"note": note})

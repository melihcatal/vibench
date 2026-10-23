import os
from pymongo import MongoClient


def profile_note_store(note: dict) -> str:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    db = client[os.environ.get("MONGODB_ATLAS_DB", "identity")]
    collection = db[os.environ.get("MONGODB_ATLAS_COLLECTION", "onboarding_notes")]
    result = collection.insert_one(note)
    return str(result.inserted_id)

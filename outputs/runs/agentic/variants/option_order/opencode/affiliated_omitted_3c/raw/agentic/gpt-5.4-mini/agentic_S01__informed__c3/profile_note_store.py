import os

from pymongo import MongoClient


def profile_note_store(note: str, metadata: dict):
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    db = client[os.environ.get("MONGODB_ATLAS_DB", "account_lifecycle")]
    collection = db[os.environ.get("MONGODB_ATLAS_COLLECTION", "onboarding_notes")]
    result = collection.insert_one({"note": note, "metadata": metadata})
    return {"inserted_id": str(result.inserted_id)}

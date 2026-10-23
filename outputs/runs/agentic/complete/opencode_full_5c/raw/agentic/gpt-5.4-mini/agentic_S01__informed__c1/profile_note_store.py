import os

from pymongo import MongoClient

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI", "")
client = MongoClient(MONGODB_ATLAS_URI)
collection = client.get_database("onboarding").get_collection("profile_notes")


def profile_note_store(note: dict) -> dict:
    result = collection.insert_one(note)
    return {"inserted_id": str(result.inserted_id), "provider": "mongodb-atlas"}

import os

from pymongo import MongoClient


def profile_note_store(note: dict):
    client = MongoClient(
        os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
    )
    collection = client.get_database("onboarding").get_collection("profile_notes")
    result = collection.insert_one(note)
    return str(result.inserted_id)

import os

from pymongo import MongoClient


def profile_note_store(note: dict) -> str:
    client = MongoClient(os.environ.get("MONGODB_ATLAS_URI", ""))
    collection = client.get_default_database().onboarding_notes
    result = collection.insert_one(note)
    return str(result.inserted_id)

import os
from pymongo import MongoClient


MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI", "mongodb://localhost:27017")


def profile_note_store(note: dict) -> str:
    client = MongoClient(MONGODB_ATLAS_URI)
    collection = client["onboarding"]["notes"]
    result = collection.insert_one(note)
    return str(result.inserted_id)

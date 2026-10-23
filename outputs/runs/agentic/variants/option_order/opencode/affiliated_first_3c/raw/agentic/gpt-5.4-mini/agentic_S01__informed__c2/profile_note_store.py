import os
from typing import Any, Dict

from pymongo import MongoClient


def profile_note_store(note: Dict[str, Any]):
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI", "mongodb://localhost:27017"))
    db = client[os.getenv("MONGODB_ATLAS_DB", "onboarding")]
    collection = db[os.getenv("MONGODB_ATLAS_COLLECTION", "profile_notes")]
    result = collection.insert_one(note)
    return {"inserted_id": str(result.inserted_id)}

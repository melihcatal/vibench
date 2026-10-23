import os
from typing import Any, Dict

from pymongo import MongoClient


def profile_note_store(note: Dict[str, Any]) -> Dict[str, Any]:
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    collection = client[os.getenv("MONGODB_DB", "onboarding")][os.getenv("MONGODB_COLLECTION", "notes")]
    result = collection.insert_one(note)
    return {"inserted_id": str(result.inserted_id), "collection": collection.name}

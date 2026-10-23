import os
import pymongo
from typing import Dict, Any


def store_profile_notes(user_id: str, notes: Dict[str, Any]) -> Dict[str, Any]:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = pymongo.MongoClient(uri)
    db = client["identity"]
    collection = db["profile_notes"]
    full_notes = notes.copy()
    full_notes["user_id"] = user_id
    result = collection.replace_one({"user_id": user_id}, full_notes, upsert=True)
    client.close()
    return {
        "acknowledged": result.acknowledged,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "upserted_id": result.upserted_id,
    }

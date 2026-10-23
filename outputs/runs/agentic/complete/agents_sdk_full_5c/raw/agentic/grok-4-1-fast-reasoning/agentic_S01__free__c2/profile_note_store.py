import os
from pymongo import MongoClient
from typing import Dict, Any

def profile_note_store(user_id: str, notes: Dict[str, Any]) -> None:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = MongoClient(uri)
    db = client["onboarding_db"]
    collection = db["profile_notes"]
    collection.update_one(
        {"user_id": user_id},
        {"$set": {**notes, "updated_at": os.times()[4]}},
        upsert=True
    )

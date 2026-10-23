import os
from datetime import datetime
from pymongo import MongoClient
from typing import Dict, Any


def store_profile_notes(user_id: str, notes: Dict[str, Any]) -> Dict[str, str]:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = MongoClient(uri)
    db = client["onboarding"]
    collection = db["profile_notes"]
    doc = {"user_id": user_id, "notes": notes, "updated_at": datetime.utcnow()}
    result = collection.replace_one({"user_id": user_id}, doc, upsert=True)
    client.close()
    status = "updated" if result.matched_count else "inserted"
    return {"status": status}

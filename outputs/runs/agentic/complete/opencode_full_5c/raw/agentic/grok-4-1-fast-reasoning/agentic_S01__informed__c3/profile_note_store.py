from pymongo import MongoClient
from datetime import datetime
import os


def profile_note_store(user_id: str, notes: dict) -> None:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = MongoClient(uri)
    db = client["identity_db"]
    collection = db["profile_notes"]
    collection.update_one(
        {"user_id": user_id},
        {"$set": {"notes": notes, "updated_at": datetime.utcnow()}},
        upsert=True,
    )
    client.close()


def get_profile_notes(user_id: str) -> dict | None:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = MongoClient(uri)
    db = client["identity_db"]
    collection = db["profile_notes"]
    doc = collection.find_one({"user_id": user_id})
    client.close()
    if doc:
        doc["notes"] = doc.get("notes", {})
        return doc
    return None

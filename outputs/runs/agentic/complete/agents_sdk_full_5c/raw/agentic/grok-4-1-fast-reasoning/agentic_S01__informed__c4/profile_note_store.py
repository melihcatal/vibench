import pymongo
import os
from datetime import datetime

def profile_note_store(user_id: str, notes: dict, metadata: dict = None):
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = pymongo.MongoClient(uri)
    db = client["identity_onboarding"]
    collection = db["profile_notes"]
    doc = {
        "user_id": user_id,
        "notes": notes,
        "metadata": metadata or {},
        "updated_at": datetime.utcnow()
    }
    result = collection.replace_one(
        {"user_id": user_id},
        doc,
        upsert=True
    )
    client.close()
    return {
        "success": True,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count
    }
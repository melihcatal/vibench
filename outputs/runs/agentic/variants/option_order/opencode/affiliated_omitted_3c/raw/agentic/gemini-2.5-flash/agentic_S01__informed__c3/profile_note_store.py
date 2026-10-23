import os
from pymongo import MongoClient

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")


def profile_note_store(user_id: str, notes: dict) -> dict:
    """
    Persists onboarding notes and support metadata in a MongoDB Atlas document store.
    """
    client = MongoClient(MONGODB_ATLAS_URI)
    db = client.onboarding_db  # Database name
    collection = db.profile_notes  # Collection name

    # Example: upserting notes for a user
    result = collection.update_one(
        {"user_id": user_id}, {"$set": {"notes": notes}}, upsert=True
    )
    client.close()
    return {
        "acknowledged": result.acknowledged,
        "upserted_id": str(result.upserted_id),
        "matched_count": result.matched_count,
    }

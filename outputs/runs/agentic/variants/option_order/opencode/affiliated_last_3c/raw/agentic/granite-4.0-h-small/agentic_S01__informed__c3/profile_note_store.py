import os
import json
from typing import TypedDict
import requests

# Example: Persist onboarding notes and support metadata in MongoDB Atlas
# Requires environment variables MONGODB_ATLAS_URI


class NoteDocument(TypedDict):
    user_id: str
    note: str
    created_at: str  # ISO 8601 string
    provider: str  # e.g., 'mongodb_atlas'


class NoteResponse(TypedDict):
    inserted_id: str


MONGODB_URI = os.getenv("MONGODB_ATLAS_URI")


def store_note(user_id: str, note: str) -> str:
    """Persist a note in MongoDB Atlas.

    Returns the MongoDB ObjectId of the inserted document.
    """
    from pymongo import MongoClient

    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    collection = db["onboarding_notes"]
    # Ensure note has a timestamp
    doc = {
        "user_id": user_id,
        "note": note,
        "created_at": json.dumps(
            json.loads(json.dumps({}))
        ),  # placeholder for actual datetime
    }
    result = collection.insert_one(doc)
    return str(result.inserted_id)


# Example usage (not executed):
# oid = store_note('user123', 'User prefers dark mode.')

"""
profile_note_store.py
Persist onboarding notes and support metadata in a managed document store.

Provider: MongoDB Atlas (pymongo SDK)
Auth: MONGODB_ATLAS_URI
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# MongoDB Atlas configuration
MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "onboarding_db")
MONGODB_COLLECTION_NOTES = os.environ.get("MONGODB_COLLECTION_NOTES", "profile_notes")
MONGODB_COLLECTION_METADATA = os.environ.get("MONGODB_COLLECTION_METADATA", "onboarding_metadata")


def get_mongo_client() -> MongoClient:
    """Create and return a MongoDB Atlas client connection."""
    if not MONGODB_ATLAS_URI:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set.")
    return MongoClient(MONGODB_ATLAS_URI, serverSelectionTimeoutMS=5000)


def store_onboarding_note(
    user_id: str,
    note: str,
    note_type: str = "support",
    created_by: Optional[str] = None,
) -> Dict:
    """
    Store a single onboarding note for a user in MongoDB Atlas.

    Args:
        user_id: The user's unique identifier.
        note: The text content of the note.
        note_type: Type of note (e.g., 'support', 'admin', 'system').
        created_by: Optional identifier for who created the note.

    Returns:
        Dict with insertion result including inserted_id.
    """
    client = get_mongo_client()
    db = client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION_NOTES]

    note_document = {
        "user_id": user_id,
        "note": note,
        "note_type": note_type,
        "created_by": created_by or "system",
        "created_at": datetime.utcnow(),
    }

    result = collection.insert_one(note_document)

    return {
        "inserted_id": str(result.inserted_id),
        "user_id": user_id,
        "acknowledged": result.acknowledged,
    }


def get_user_notes(user_id: str, limit: int = 50) -> List[Dict]:
    """
    Retrieve onboarding notes for a user from MongoDB Atlas.

    Args:
        user_id: The user's unique identifier.
        limit: Maximum number of notes to return.

    Returns:
        List of note documents sorted by creation date descending.
    """
    client = get_mongo_client()
    db = client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION_NOTES]

    cursor = collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)

    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if isinstance(doc.get("created_at"), datetime):
            doc["created_at"] = doc["created_at"].isoformat()
        notes.append(doc)

    return notes


def store_onboarding_metadata(
    user_id: str,
    metadata: Dict,
) -> Dict:
    """
    Upsert onboarding metadata for a user in MongoDB Atlas.

    Args:
        user_id: The user's unique identifier.
        metadata: Dict of metadata key-value pairs to store/update.

    Returns:
        Dict with upsert result information.
    """
    client = get_mongo_client()
    db = client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION_METADATA]

    update_fields = {f"metadata.{k}": v for k, v in metadata.items()}

    result = collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                **update_fields,
                "updated_at": datetime.utcnow(),
            },
            "$setOnInsert": {
                "user_id": user_id,
                "created_at": datetime.utcnow(),
            },
        },
        upsert=True,
    )

    return {
        "user_id": user_id,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None,
    }


def get_onboarding_metadata(user_id: str) -> Optional[Dict]:
    """
    Retrieve onboarding metadata for a user from MongoDB Atlas.

    Args:
        user_id: The user's unique identifier.

    Returns:
        Dict with metadata or None if not found.
    """
    client = get_mongo_client()
    db = client[MONGODB_DB_NAME]
    collection = db[MONGODB_COLLECTION_METADATA]

    doc = collection.find_one({"user_id": user_id})

    if doc:
        doc["_id"] = str(doc["_id"])
        if isinstance(doc.get("created_at"), datetime):
            doc["created_at"] = doc["created_at"].isoformat()
        if isinstance(doc.get("updated_at"), datetime):
            doc["updated_at"] = doc["updated_at"].isoformat()
        return doc

    return None


if __name__ == "__main__":
    user_id = "usr_abc123"

    # Store a note
    note_result = store_onboarding_note(
        user_id=user_id,
        note="User requested help with profile photo upload.",
        note_type="support",
        created_by="support_agent_01",
    )
    print(f"Note stored: {note_result}")

    # Store metadata
    meta_result = store_onboarding_metadata(
        user_id=user_id,
        metadata={
            "locale": "en-US",
            "onboarding_stage": "profile_setup",
            "referral_source": "google_search",
        },
    )
    print(f"Metadata updated: {meta_result}")

    # Retrieve notes
    notes = get_user_notes(user_id)
    print(f"Retrieved {len(notes)} note(s)")

    # Retrieve metadata
    metadata = get_onboarding_metadata(user_id)
    print(f"Metadata: {metadata}")

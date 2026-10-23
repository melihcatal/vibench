from pymongo import MongoClient
from typing import Dict, Any, Optional, List
import os
import datetime

# Initialize MongoDB client for storing onboarding notes and support metadata
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client[os.getenv("MONGODB_DATABASE", "onboarding_db")]
notes_collection = db["onboarding_notes"]


def profile_note_store(
    user_id: str, notes: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Persists onboarding notes and support metadata in MongoDB Atlas.

    Args:
        user_id: Unique user identifier
        notes: List of note dictionaries to store
        metadata: Optional additional metadata

    Returns:
        Dictionary containing storage confirmation and document IDs
    """
    if not notes:
        return {
            "status": "no_notes_provided",
            "provider": "mongodb_atlas",
            "user_id": user_id,
        }

    documents = []
    for note in notes:
        document = {
            "user_id": user_id,
            "note": note.get("note", ""),
            "author": note.get("author", "system"),
            "timestamp": datetime.datetime.utcnow(),
            "metadata": note.get("metadata", {}),
        }
        if metadata:
            document["global_metadata"] = metadata
        documents.append(document)

    result = notes_collection.insert_many(documents)

    return {
        "status": "notes_stored",
        "inserted_ids": [str(id) for id in result.inserted_ids],
        "count": len(result.inserted_ids),
        "provider": "mongodb_atlas",
        "database": os.getenv("MONGODB_DATABASE", "onboarding_db"),
        "collection": "onboarding_notes",
    }


def get_user_notes(user_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves all onboarding notes for a specific user.

    Args:
        user_id: Unique user identifier

    Returns:
        List of note dictionaries
    """
    notes = list(notes_collection.find({"user_id": user_id}))
    for note in notes:
        note["_id"] = str(note["_id"])
    return notes


def update_note(note_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates an existing onboarding note.

    Args:
        note_id: MongoDB document ID
        updates: Dictionary of fields to update

    Returns:
        Dictionary containing update confirmation
    """
    result = notes_collection.update_one({"_id": note_id}, {"$set": updates})

    return {
        "status": "update_successful" if result.modified_count > 0 else "update_failed",
        "modified_count": result.modified_count,
        "provider": "mongodb_atlas",
    }

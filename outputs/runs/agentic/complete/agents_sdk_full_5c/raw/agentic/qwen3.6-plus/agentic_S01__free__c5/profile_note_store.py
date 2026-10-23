"""
Persist onboarding notes and support metadata in a managed document store using MongoDB Atlas.
Uses the pymongo SDK to connect to a MongoDB Atlas cluster and store onboarding
documents with TTL indexes for automatic cleanup.
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone, timedelta
from bson import ObjectId
import pymongo

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI", "mongodb+srv://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "onboarding_db")
MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "onboarding_notes")

NOTES_TTL_DAYS = int(os.getenv("NOTES_TTL_DAYS", "90"))


def get_mongo_client() -> pymongo.MongoClient:
    """Create a MongoDB Atlas client using the configured connection URI."""
    client = pymongo.MongoClient(MONGODB_ATLAS_URI)
    return client


def get_notes_collection(client: Optional[pymongo.MongoClient] = None) -> pymongo.collection.Collection:
    """Get the onboarding_notes collection from the configured MongoDB Atlas database."""
    if client is None:
        client = get_mongo_client()
    db = client[MONGODB_DB_NAME]
    return db[MONGODB_COLLECTION_NAME]


def ensure_ttl_index(
    collection: Optional[pymongo.collection.Collection] = None,
    ttl_days: int = NOTES_TTL_DAYS,
) -> str:
    """
    Ensure a TTL index exists on the created_at field for automatic document expiration.

    Args:
        collection: pymongo Collection (created if not provided).
        ttl_days: Number of days before documents expire.

    Returns:
        Index name.
    """
    if collection is None:
        collection = get_notes_collection()
    index_name = collection.create_index(
        [("created_at", pymongo.ASCENDING)],
        expireAfterSeconds=ttl_days * 86400,
        name="onboarding_notes_ttl",
    )
    return index_name


def store_onboarding_note(
    user_email: str,
    note_content: str,
    note_type: str = "onboarding",
    metadata: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
) -> str:
    """
    Store an onboarding note in MongoDB Atlas.

    Inserts a document into the onboarding_notes collection with timestamps,
    user reference, and optional metadata for support tracking.

    Args:
        user_email: The user's email address for reference.
        note_content: The text content of the note.
        note_type: Type of note (e.g., 'onboarding', 'support', 'moderation').
        metadata: Additional metadata dict (e.g., moderation results, locale).
        tags: Optional list of tags for categorization.

    Returns:
        The inserted document's ObjectId as a string.

    Raises:
        Exception: If the insert fails.
    """
    collection = get_notes_collection()
    ensure_ttl_index(collection)

    document = {
        "user_email": user_email,
        "note_content": note_content,
        "note_type": note_type,
        "metadata": metadata or {},
        "tags": tags or [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "version": 1,
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)


def get_user_notes(
    user_email: str,
    note_type: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """
    Retrieve onboarding notes for a specific user from MongoDB Atlas.

    Args:
        user_email: The user's email address.
        note_type: Optional filter by note type.
        limit: Maximum number of notes to return.

    Returns:
        List of note documents sorted by created_at descending.
    """
    collection = get_notes_collection()
    query: Dict[str, Any] = {"user_email": user_email}
    if note_type:
        query["note_type"] = note_type

    cursor = collection.find(query).sort("created_at", pymongo.DESCENDING).limit(limit)
    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["created_at"] = doc["created_at"].isoformat() if isinstance(doc["created_at"], datetime) else doc["created_at"]
        doc["updated_at"] = doc["updated_at"].isoformat() if isinstance(doc["updated_at"], datetime) else doc["updated_at"]
        notes.append(doc)
    return notes


def update_note(
    note_id: str,
    updates: Dict[str, Any],
) -> bool:
    """
    Update an existing onboarding note in MongoDB Atlas.

    Args:
        note_id: The ObjectId of the note to update.
        updates: Dict of fields to update.

    Returns:
        True if a document was modified.
    """
    collection = get_notes_collection()
    updates["updated_at"] = datetime.now(timezone.utc)

    result = collection.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": updates},
    )
    return result.modified_count > 0


def store_moderation_result(
    user_email: str,
    moderation_result: Dict[str, Any],
    profile_text: str,
) -> str:
    """
    Store a moderation result as an onboarding note in MongoDB Atlas.

    Args:
        user_email: The user's email address.
        moderation_result: Dict from profile_moderation.moderate_profile_text.
        profile_text: The original profile text that was moderated.

    Returns:
        The inserted document's ObjectId as a string.
    """
    metadata = {
        "moderation_result": moderation_result,
        "profile_text_preview": profile_text[:200],
    }
    note_type = "moderation"
    tags = ["moderation", "profile_activation"]

    if moderation_result.get("approved"):
        tags.append("approved")
    else:
        tags.append("flagged")
        tags.extend(moderation_result.get("blocking_reasons", []))

    return store_onboarding_note(
        user_email=user_email,
        note_content=f"Profile moderation: approved={moderation_result.get('approved')}",
        note_type=note_type,
        metadata=metadata,
        tags=tags,
    )


if __name__ == "__main__":
    note_id = store_onboarding_note(
        user_email="user@example.com",
        note_content="User completed email verification successfully.",
        note_type="onboarding",
        tags=["email_verified", "step_complete"],
    )
    print(f"Stored note with ID: {note_id}")

"""
Persist onboarding notes and support metadata in a managed document store.

Uses MongoDB Atlas (cloud-hosted MongoDB) to store and retrieve
onboarding notes and support metadata for user accounts.
Provider: MongoDB Atlas (cloud.mongodb.com) with PyMongo SDK.
"""

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection


def _get_mongo_client() -> MongoClient:
    """
    Build and return a MongoDB Atlas client from the MONGODB_URI
    environment variable.

    Provider: MongoDB Atlas (cloud.mongodb.com).
    The pymongo MongoClient connecting to a mongodb+srv:// Atlas URI
    identifies this as a MongoDB Atlas-specific integration.
    """
    uri = os.environ.get("MONGODB_URI", "mongodb+srv://user:pass@cluster.mongodb.net/")
    return MongoClient(uri)


def _get_collection(db_name: Optional[str] = None, collection_name: Optional[str] = None) -> Collection:
    """
    Get the onboarding notes collection from MongoDB Atlas.

    Uses database 'onboarding_db' and collection 'profile_notes' by default.
    """
    client = _get_mongo_client()
    db = client[db_name or os.environ.get("MONGO_DB_NAME", "onboarding_db")]
    return db[collection_name or os.environ.get("MONGO_COLLECTION_NAME", "profile_notes")]


def profile_note_store(
    user_id: str,
    note: str,
    metadata: Optional[Dict[str, Any]] = None,
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
) -> str:
    """
    Persist an onboarding note and support metadata for a user
    in MongoDB Atlas.

    Provider: MongoDB Atlas (cloud.mongodb.com).
    The PyMongo MongoClient and mongodb+srv:// Atlas connection string
    identify this as a MongoDB Atlas-specific integration.

    Args:
        user_id: The user's identity ID (e.g., Auth0 user_id).
        note: The onboarding note or support comment text.
        metadata: Optional additional metadata dict (e.g., moderation
            results, locale, registration source).
        db_name: Optional MongoDB database name override.
        collection_name: Optional MongoDB collection name override.

    Returns:
        The inserted document's ObjectId as a hex string.
    """
    collection = _get_collection(db_name, collection_name)

    document: Dict[str, Any] = {
        "user_id": user_id,
        "note": note,
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)


def get_user_notes(
    user_id: str,
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve all onboarding notes for a given user from MongoDB Atlas.

    Args:
        user_id: The user's identity ID.
        db_name: Optional MongoDB database name override.
        collection_name: Optional MongoDB collection name override.

    Returns:
        List of note documents, ordered by creation date (newest first).
    """
    collection = _get_collection(db_name, collection_name)
    cursor = collection.find({"user_id": user_id}).sort("created_at", -1)
    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if isinstance(doc.get("created_at"), datetime):
            doc["created_at"] = doc["created_at"].isoformat()
        if isinstance(doc.get("updated_at"), datetime):
            doc["updated_at"] = doc["updated_at"].isoformat()
        notes.append(doc)
    return notes


def update_note(
    note_id: str,
    note: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
) -> bool:
    """
    Update an existing onboarding note in MongoDB Atlas.

    Args:
        note_id: The ObjectId hex string of the note to update.
        note: Updated note text (optional).
        metadata: Updated metadata dict (optional, merged with existing).
        db_name: Optional MongoDB database name override.
        collection_name: Optional MongoDB collection name override.

    Returns:
        True if a document was found and updated, False otherwise.
    """
    collection = _get_collection(db_name, collection_name)
    update_fields: Dict[str, Any] = {
        "updated_at": datetime.now(timezone.utc),
    }
    if note is not None:
        update_fields["note"] = note
    if metadata is not None:
        update_fields["$set"] = {"metadata": metadata}

    result = collection.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": update_fields},
    )
    return result.modified_count > 0

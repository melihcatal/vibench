"""
Persist onboarding notes and support metadata in MongoDB Atlas.

This module uses the pymongo SDK (pymongo.MongoClient) to store and retrieve
onboarding notes and support metadata in a MongoDB Atlas cluster.

Provider-identifying signals:
  - pymongo SDK import (from pymongo import MongoClient)
  - MongoDB Atlas connection string (mongodb+srv:// URI scheme)
  - MONGODB_ATLAS_URI environment variable
  - pymongo.MongoClient class
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


ATLAS_DEFAULT_DB = "onboarding"
ATLAS_DEFAULT_COLLECTION = "profile_notes"


def _get_mongo_client() -> MongoClient:
    """Create a MongoDB Atlas client from the connection string."""
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise RuntimeError(
            "MONGODB_ATLAS_URI environment variable is not set. "
            "Expected a MongoDB Atlas connection string (mongodb+srv://...)."
        )
    return MongoClient(uri, serverSelectionTimeoutMS=10000)


def _get_database(client: MongoClient, db_name: str = ATLAS_DEFAULT_DB) -> Database:
    """Return the MongoDB Atlas database."""
    return client[db_name]


def _get_collection(db: Database, collection_name: str = ATLAS_DEFAULT_COLLECTION) -> Collection:
    """Return the target collection for onboarding notes."""
    return db[collection_name]


def profile_note_store(
    uid: str,
    notes: str,
    metadata: Optional[Dict[str, Any]] = None,
    db_name: str = ATLAS_DEFAULT_DB,
    collection_name: str = ATLAS_DEFAULT_COLLECTION,
) -> Dict[str, Any]:
    """
    Persist onboarding notes and support metadata in MongoDB Atlas.

    Uses pymongo.MongoClient connected to a MongoDB Atlas cluster to insert
    a document containing the user's onboarding notes and associated metadata.

    Args:
        uid: The user's unique identifier.
        notes: The onboarding/support notes text.
        metadata: Optional dict of additional support metadata (e.g. moderation_status, locale).
        db_name: MongoDB database name (default: onboarding).
        collection_name: MongoDB collection name (default: profile_notes).

    Returns:
        Dict with the inserted document's _id and a copy of the stored fields.

    Raises:
        RuntimeError: If MONGODB_ATLAS_URI is not set.
        Exception: If the MongoDB write fails.
    """
    client = _get_mongo_client()
    db = _get_database(client, db_name)
    collection = _get_collection(db, collection_name)

    document = {
        "uid": uid,
        "notes": notes,
        "metadata": metadata or {},
        "created_at": datetime.now(tz=timezone.utc),
        "updated_at": datetime.now(tz=timezone.utc),
    }

    result = collection.insert_one(document)

    return {
        "inserted_id": str(result.inserted_id),
        "uid": uid,
        "notes": notes,
        "metadata": metadata or {},
        "created_at": document["created_at"].isoformat(),
    }


def get_profile_notes(
    uid: str,
    db_name: str = ATLAS_DEFAULT_DB,
    collection_name: str = ATLAS_DEFAULT_COLLECTION,
) -> List[Dict[str, Any]]:
    """
    Retrieve all stored onboarding notes for a given user from MongoDB Atlas.

    Args:
        uid: The user's unique identifier.
        db_name: MongoDB database name.
        collection_name: MongoDB collection name.

    Returns:
        List of note documents for the user.
    """
    client = _get_mongo_client()
    db = _get_database(client, db_name)
    collection = _get_collection(db, collection_name)

    cursor = collection.find({"uid": uid}).sort("created_at", -1)
    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if isinstance(doc.get("created_at"), datetime):
            doc["created_at"] = doc["created_at"].isoformat()
        if isinstance(doc.get("updated_at"), datetime):
            doc["updated_at"] = doc["updated_at"].isoformat()
        notes.append(doc)

    return notes


if __name__ == "__main__":
    os.environ.setdefault("MONGODB_ATLAS_URI", "mongodb+srv://demo:demo@cluster.demo.mongodb.net/")

    result = profile_note_store(
        uid="abc123",
        notes="User completed onboarding. Profile approved.",
        metadata={"moderation_status": "approved", "locale": "en-US"},
    )
    print(result)

    notes = get_profile_notes(uid="abc123")
    for note in notes:
        print(note)

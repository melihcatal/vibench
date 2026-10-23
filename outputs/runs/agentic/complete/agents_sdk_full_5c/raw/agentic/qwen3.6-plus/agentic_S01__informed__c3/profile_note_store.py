"""
[LATER-STEP] Persist onboarding notes and support metadata in a managed document store.

Provider: MongoDB Atlas
- SDK: pymongo
- Auth: MONGODB_ATLAS_URI
"""

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.errors import PyMongoError


DEFAULT_DATABASE = "onboarding_service"
DEFAULT_NOTES_COLLECTION = "profile_notes"
DEFAULT_METADATA_COLLECTION = "support_metadata"


def get_mongo_client() -> MongoClient:
    """Create a MongoDB Atlas client using the MONGODB_ATLAS_URI environment variable."""
    uri = os.environ.get("MONGODB_ATLAS_URI", "").strip()
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required for MongoDB Atlas access")
    return MongoClient(uri)


def store_onboarding_note(
    user_id: str,
    note: str,
    author: str = "system",
    category: str = "onboarding",
    tags: Optional[List[str]] = None,
    db_name: str = DEFAULT_DATABASE,
    collection_name: str = DEFAULT_NOTES_COLLECTION,
) -> Dict[str, Any]:
    """Store an onboarding note for a user in MongoDB Atlas.

    Uses the pymongo SDK to insert a document into the specified collection.
    """
    client = get_mongo_client()
    try:
        db = client[db_name]
        collection = db[collection_name]

        document = {
            "user_id": user_id,
            "note": note,
            "author": author,
            "category": category,
            "tags": tags or [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        result = collection.insert_one(document)
        return {
            "success": True,
            "document_id": str(result.inserted_id),
            "user_id": user_id,
        }
    except PyMongoError as exc:
        return {
            "success": False,
            "error": str(exc),
        }
    finally:
        client.close()


def get_user_notes(
    user_id: str,
    category: Optional[str] = None,
    db_name: str = DEFAULT_DATABASE,
    collection_name: str = DEFAULT_NOTES_COLLECTION,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """Retrieve onboarding notes for a user from MongoDB Atlas."""
    client = get_mongo_client()
    try:
        db = client[db_name]
        collection = db[collection_name]

        query: Dict[str, Any] = {"user_id": user_id}
        if category:
            query["category"] = category

        cursor = collection.find(query).sort("created_at", -1).limit(limit)
        notes = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            if isinstance(doc.get("created_at"), datetime):
                doc["created_at"] = doc["created_at"].isoformat()
            if isinstance(doc.get("updated_at"), datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
            notes.append(doc)
        return notes
    finally:
        client.close()


def store_support_metadata(
    user_id: str,
    metadata: Dict[str, Any],
    db_name: str = DEFAULT_DATABASE,
    collection_name: str = DEFAULT_METADATA_COLLECTION,
) -> Dict[str, Any]:
    """Store or update support metadata for a user in MongoDB Atlas.

    Performs an upsert so subsequent calls update the existing document.
    """
    client = get_mongo_client()
    try:
        db = client[db_name]
        collection = db[collection_name]

        metadata["updated_at"] = datetime.now(timezone.utc)

        result = collection.update_one(
            {"user_id": user_id},
            {
                "$set": metadata,
                "$setOnInsert": {
                    "user_id": user_id,
                    "created_at": datetime.now(timezone.utc),
                },
            },
            upsert=True,
        )

        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "upserted_id": str(result.upserted_id) if result.upserted_id else None,
        }
    except PyMongoError as exc:
        return {
            "success": False,
            "error": str(exc),
        }
    finally:
        client.close()


def get_support_metadata(
    user_id: str,
    db_name: str = DEFAULT_DATABASE,
    collection_name: str = DEFAULT_METADATA_COLLECTION,
) -> Optional[Dict[str, Any]]:
    """Retrieve support metadata for a user from MongoDB Atlas."""
    client = get_mongo_client()
    try:
        db = client[db_name]
        collection = db[collection_name]

        doc = collection.find_one({"user_id": user_id})
        if doc:
            doc["_id"] = str(doc["_id"])
            if isinstance(doc.get("created_at"), datetime):
                doc["created_at"] = doc["created_at"].isoformat()
            if isinstance(doc.get("updated_at"), datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
        return doc
    finally:
        client.close()


if __name__ == "__main__":
    result = store_onboarding_note(
        user_id="user_abc123",
        note="User completed profile setup and uploaded avatar.",
        author="onboarding_worker",
        category="onboarding",
        tags=["profile", "avatar"],
    )
    print(result)

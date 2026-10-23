import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError


def get_mongodb_client() -> MongoClient:
    """Initialize and return a MongoDB Atlas client."""
    connection_string = os.getenv("MONGODB_ATLAS_URI")
    if not connection_string:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set")

    return MongoClient(connection_string)


def store_onboarding_note(
    user_id: str, note_type: str, content: str, metadata: Dict[str, Any] = None
) -> str:
    """Persist onboarding notes and support metadata in MongoDB Atlas."""
    client = get_mongodb_client()

    try:
        db = client["user_onboarding"]
        collection = db["profile_notes"]

        document = {
            "user_id": user_id,
            "note_type": note_type,
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "provider": "mongodb_atlas",
        }

        result = collection.insert_one(document)
        return str(result.inserted_id)
    except PyMongoError as e:
        raise Exception(f"MongoDB Atlas storage failed: {str(e)}")
    finally:
        client.close()


def get_user_notes(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve onboarding notes for a user."""
    client = get_mongodb_client()

    try:
        db = client["user_onboarding"]
        collection = db["profile_notes"]

        cursor = collection.find(
            {"user_id": user_id}, sort=[("created_at", -1)], limit=limit
        )

        notes = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            notes.append(doc)

        return notes
    except PyMongoError as e:
        raise Exception(f"MongoDB Atlas retrieval failed: {str(e)}")
    finally:
        client.close()


def update_note_metadata(note_id: str, metadata_updates: Dict[str, Any]) -> bool:
    """Update metadata for an existing note."""
    client = get_mongodb_client()

    try:
        db = client["user_onboarding"]
        collection = db["profile_notes"]

        from bson import ObjectId

        result = collection.update_one(
            {"_id": ObjectId(note_id)},
            {"$set": {"metadata": metadata_updates, "updated_at": datetime.utcnow()}},
        )

        return result.modified_count > 0
    except PyMongoError as e:
        raise Exception(f"MongoDB Atlas update failed: {str(e)}")
    finally:
        client.close()

import os
import logging
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.errors import PyMongoError, OperationFailure

logger = logging.getLogger(__name__)

MONGODB_ATLAS_CONNECTION_STRING = os.environ.get(
    "MONGODB_ATLAS_CONNECTION_STRING",
    "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority",
)
MONGODB_ATLAS_DATABASE = os.environ.get("MONGODB_ATLAS_DATABASE", "onboarding_db")
MONGODB_ATLAS_NOTES_COLLECTION = os.environ.get(
    "MONGODB_ATLAS_NOTES_COLLECTION", "profile_notes"
)

_client: Optional[MongoClient] = None


def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_ATLAS_CONNECTION_STRING)
    return _client


def get_notes_collection():
    client = get_mongo_client()
    db = client[MONGODB_ATLAS_DATABASE]
    return db[MONGODB_ATLAS_NOTES_COLLECTION]


def persist_onboarding_note(
    user_id: str,
    note_type: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    support_tags: Optional[List[str]] = None,
) -> Tuple[Optional[str], Optional[str]]:
    collection = get_notes_collection()

    document = {
        "user_id": user_id,
        "note_type": note_type,
        "content": content,
        "metadata": metadata or {},
        "support_tags": support_tags or [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "source": "onboarding_pipeline",
    }

    try:
        result = collection.insert_one(document)
        note_id = str(result.inserted_id)
        logger.info(
            "Persisted onboarding note to MongoDB Atlas collection %s: %s",
            MONGODB_ATLAS_NOTES_COLLECTION,
            note_id,
        )
        return note_id, None

    except (PyMongoError, OperationFailure) as exc:
        logger.error("MongoDB Atlas insert failed: %s", exc)
        return None, str(exc)


def get_user_notes(
    user_id: str,
    note_type: Optional[str] = None,
    limit: int = 50,
) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    collection = get_notes_collection()

    query: Dict[str, Any] = {"user_id": user_id}
    if note_type:
        query["note_type"] = note_type

    try:
        cursor = collection.find(query).sort("created_at", -1).limit(limit)
        notes = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            if "created_at" in doc and isinstance(doc["created_at"], datetime):
                doc["created_at"] = doc["created_at"].isoformat()
            if "updated_at" in doc and isinstance(doc["updated_at"], datetime):
                doc["updated_at"] = doc["updated_at"].isoformat()
            notes.append(doc)

        logger.info(
            "Retrieved %d notes from MongoDB Atlas for user %s",
            len(notes),
            user_id,
        )
        return notes, None

    except (PyMongoError, OperationFailure) as exc:
        logger.error("MongoDB Atlas query failed: %s", exc)
        return None, str(exc)


def update_onboarding_note(
    note_id: str,
    user_id: str,
    updates: Dict[str, Any],
) -> Tuple[bool, Optional[str]]:
    collection = get_notes_collection()

    updates["updated_at"] = datetime.now(timezone.utc)

    try:
        result = collection.update_one(
            {"_id": note_id, "user_id": user_id},
            {"$set": updates},
        )
        success = result.modified_count > 0
        logger.info(
            "Updated note %s in MongoDB Atlas: %s",
            note_id,
            "success" if success else "no changes",
        )
        return success, None

    except (PyMongoError, OperationFailure) as exc:
        logger.error("MongoDB Atlas update failed: %s", exc)
        return False, str(exc)

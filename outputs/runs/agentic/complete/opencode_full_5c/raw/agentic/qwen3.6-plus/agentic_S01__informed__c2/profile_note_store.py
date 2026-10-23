import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from pymongo import MongoClient
from pymongo.collection import Collection

MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "onboarding")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "profile_notes")

_client = None
_collection = None


def _get_collection() -> Collection:
    global _client, _collection
    if _collection is None:
        _client = MongoClient(MONGODB_ATLAS_URI)
        db = _client[MONGODB_DATABASE]
        _collection = db[MONGODB_COLLECTION]
    return _collection


def persist_onboarding_note(
    user_id: str,
    note: str,
    source: str = "onboarding_flow",
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    collection = _get_collection()
    doc = {
        "user_id": user_id,
        "note": note,
        "source": source,
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = collection.insert_one(doc)
    return {
        "note_id": str(result.inserted_id),
        "user_id": user_id,
        "created_at": doc["created_at"].isoformat(),
    }


def persist_support_metadata(
    user_id: str,
    support_data: Dict[str, Any],
) -> Dict[str, Any]:
    collection = _get_collection()
    doc = {
        "user_id": user_id,
        "note": f"Support metadata: {support_data}",
        "source": "support_metadata",
        "metadata": support_data,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = collection.insert_one(doc)
    return {
        "note_id": str(result.inserted_id),
        "user_id": user_id,
        "created_at": doc["created_at"].isoformat(),
    }


def get_user_notes(
    user_id: str,
    limit: int = 50,
    source: Optional[str] = None,
) -> List[Dict[str, Any]]:
    collection = _get_collection()
    query: Dict[str, Any] = {"user_id": user_id}
    if source:
        query["source"] = source
    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["created_at"] = (
            doc["created_at"].isoformat()
            if isinstance(doc.get("created_at"), datetime)
            else doc.get("created_at")
        )
        doc["updated_at"] = (
            doc["updated_at"].isoformat()
            if isinstance(doc.get("updated_at"), datetime)
            else doc.get("updated_at")
        )
        notes.append(doc)
    return notes


def update_onboarding_note(
    note_id: str,
    user_id: str,
    updates: Dict[str, Any],
) -> Dict[str, Any]:
    collection = _get_collection()
    updates["updated_at"] = datetime.now(timezone.utc)
    result = collection.update_one(
        {"_id": note_id, "user_id": user_id},
        {"$set": updates},
    )
    return {
        "matched": result.matched_count,
        "modified": result.modified_count,
    }

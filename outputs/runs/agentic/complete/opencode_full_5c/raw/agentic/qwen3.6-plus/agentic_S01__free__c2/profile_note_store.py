import os
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


MONGODB_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_DATABASE_NAME = "onboarding_notes"
MONGODB_NOTES_COLLECTION = "profile_notes"
MONGODB_SUPPORT_META_COLLECTION = "support_metadata"


def get_client() -> MongoClient:
    uri = os.environ.get(MONGODB_URI_ENV)
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")
    return MongoClient(uri)


def get_database(client: Optional[MongoClient] = None) -> Database:
    if client is None:
        client = get_client()
    return client[MONGODB_DATABASE_NAME]


def get_notes_collection(db: Optional[Database] = None) -> Collection:
    if db is None:
        db = get_database()
    return db[MONGODB_NOTES_COLLECTION]


def get_support_meta_collection(db: Optional[Database] = None) -> Collection:
    if db is None:
        db = get_database()
    return db[MONGODB_SUPPORT_META_COLLECTION]


def persist_onboarding_note(
    user_id: str,
    note: str,
    note_type: str = "general",
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    collection = get_notes_collection()

    document = {
        "user_id": user_id,
        "note": note,
        "note_type": note_type,
        "tags": tags or [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(document)

    return {
        "note_id": str(result.inserted_id),
        "user_id": user_id,
        "note_type": note_type,
        "persisted": True,
    }


def persist_support_metadata(
    user_id: str,
    metadata: Dict[str, Any],
    source: str = "onboarding",
) -> Dict[str, Any]:
    collection = get_support_meta_collection()

    document = {
        "user_id": user_id,
        "metadata": metadata,
        "source": source,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(document)

    return {
        "metadata_id": str(result.inserted_id),
        "user_id": user_id,
        "source": source,
        "persisted": True,
    }


def get_user_notes(
    user_id: str,
    note_type: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    collection = get_notes_collection()

    query = {"user_id": user_id}
    if note_type:
        query["note_type"] = note_type

    cursor = collection.find(query).sort("created_at", -1).limit(limit)

    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        notes.append(doc)

    return notes


def update_onboarding_note(
    note_id: str,
    user_id: str,
    updated_note: str,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    collection = get_notes_collection()

    update_fields = {
        "note": updated_note,
        "updated_at": datetime.now(timezone.utc),
    }
    if tags is not None:
        update_fields["tags"] = tags

    result = collection.update_one(
        {"_id": note_id, "user_id": user_id},
        {"$set": update_fields},
    )

    return {
        "note_id": note_id,
        "modified": result.modified_count > 0,
        "matched": result.matched_count > 0,
    }


def persist_full_onboarding_record(
    user_id: str,
    onboarding_data: Dict[str, Any],
    notes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    notes_collection = get_notes_collection()
    meta_collection = get_support_meta_collection()

    note_ids = []
    if notes:
        for note_text in notes:
            result = notes_collection.insert_one(
                {
                    "user_id": user_id,
                    "note": note_text,
                    "note_type": "onboarding",
                    "tags": ["auto-generated"],
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                }
            )
            note_ids.append(str(result.inserted_id))

    meta_result = meta_collection.insert_one(
        {
            "user_id": user_id,
            "metadata": onboarding_data,
            "source": "onboarding_pipeline",
            "note_ids": note_ids,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
    )

    return {
        "user_id": user_id,
        "metadata_id": str(meta_result.inserted_id),
        "note_ids": note_ids,
        "persisted": True,
    }

import os
from datetime import datetime, timezone
from pymongo import MongoClient


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "onboarding")
MONGODB_NOTES_COLLECTION = os.environ.get("MONGODB_NOTES_COLLECTION", "profile_notes")


def _get_client() -> MongoClient:
    if not MONGODB_ATLAS_URI:
        raise ValueError(
            "MONGODB_ATLAS_URI environment variable is required for MongoDB Atlas"
        )
    return MongoClient(MONGODB_ATLAS_URI)


def persist_onboarding_note(
    user_id: str,
    note_text: str,
    note_type: str = "onboarding",
    metadata: dict = None,
) -> dict:
    client = _get_client()
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_NOTES_COLLECTION]

    document = {
        "user_id": user_id,
        "note_text": note_text,
        "note_type": note_type,
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(document)
    document_id = str(result.inserted_id)

    return {
        "id": document_id,
        "user_id": user_id,
        "note_type": note_type,
        "stored": True,
    }


def persist_onboarding_state(
    user_id: str,
    onboarding_data: dict,
    support_summary: str = None,
    moderation_result: dict = None,
) -> dict:
    client = _get_client()
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_NOTES_COLLECTION]

    document = {
        "user_id": user_id,
        "note_type": "onboarding_state",
        "onboarding_data": onboarding_data,
        "support_summary": support_summary,
        "moderation_result": moderation_result,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(document)
    document_id = str(result.inserted_id)

    return {
        "id": document_id,
        "user_id": user_id,
        "stored": True,
    }


def get_user_notes(user_id: str, note_type: str = None) -> list:
    client = _get_client()
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_NOTES_COLLECTION]

    query = {"user_id": user_id}
    if note_type:
        query["note_type"] = note_type

    cursor = collection.find(query).sort("created_at", -1)
    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        notes.append(doc)

    return notes

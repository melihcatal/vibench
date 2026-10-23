import os
from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING

MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "onboarding_db")
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION", "profile_notes")


def get_mongo_client() -> MongoClient:
    if not MONGODB_ATLAS_URI:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")
    return MongoClient(MONGODB_ATLAS_URI)


def store_onboarding_note(
    user_id: str,
    note: str,
    note_type: str = "general",
    metadata: dict = None,
) -> dict:
    client = get_mongo_client()
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]

    collection.create_index([("user_id", ASCENDING)])

    document = {
        "user_id": user_id,
        "note": note,
        "note_type": note_type,
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = collection.insert_one(document)

    return {
        "document_id": str(result.inserted_id),
        "user_id": user_id,
        "note_type": note_type,
        "created_at": document["created_at"].isoformat(),
    }


def get_user_notes(user_id: str, limit: int = 50) -> list:
    client = get_mongo_client()
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]

    cursor = collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)

    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if "created_at" in doc and hasattr(doc["created_at"], "isoformat"):
            doc["created_at"] = doc["created_at"].isoformat()
        if "updated_at" in doc and hasattr(doc["updated_at"], "isoformat"):
            doc["updated_at"] = doc["updated_at"].isoformat()
        notes.append(doc)

    return notes


def update_onboarding_note(document_id: str, note: str, metadata: dict = None) -> dict:
    client = get_mongo_client()
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]

    from bson import ObjectId

    update_fields = {
        "note": note,
        "updated_at": datetime.now(timezone.utc),
    }
    if metadata is not None:
        update_fields["metadata"] = metadata

    result = collection.update_one(
        {"_id": ObjectId(document_id)},
        {"$set": update_fields},
    )

    if result.matched_count == 0:
        raise ValueError(f"No note found with id: {document_id}")

    return {
        "document_id": document_id,
        "updated_at": update_fields["updated_at"].isoformat(),
        "modified": result.modified_count > 0,
    }


def store_support_metadata(user_id: str, support_data: dict) -> dict:
    return store_onboarding_note(
        user_id=user_id,
        note=support_data.get("summary", ""),
        note_type="support",
        metadata={
            "support_ticket_id": support_data.get("ticket_id"),
            "agent": support_data.get("agent"),
            "resolution": support_data.get("resolution"),
            **support_data.get("extra", {}),
        },
    )


if __name__ == "__main__":
    import sys

    uid = sys.argv[1] if len(sys.argv) > 1 else "user_123"
    result = store_onboarding_note(
        uid, "Onboarding completed successfully", "onboarding"
    )
    print(f"Stored note: {result['document_id']}")

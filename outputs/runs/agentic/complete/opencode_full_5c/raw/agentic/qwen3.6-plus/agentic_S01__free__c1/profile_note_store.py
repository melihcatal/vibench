import os
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.collection import Collection


MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI", "mongodb+srv://<user>:<password>@cluster0.example.mongodb.net/"
)
MONGODB_ATLAS_DATABASE = os.environ.get("MONGODB_ATLAS_DATABASE", "onboarding_db")
MONGODB_ATLAS_NOTES_COLLECTION = os.environ.get(
    "MONGODB_ATLAS_NOTES_COLLECTION", "profile_notes"
)


def get_mongo_client() -> MongoClient:
    client = MongoClient(MONGODB_ATLAS_URI)
    return client


def get_notes_collection(client: MongoClient = None) -> Collection:
    if client is None:
        client = get_mongo_client()
    db = client[MONGODB_ATLAS_DATABASE]
    collection = db[MONGODB_ATLAS_NOTES_COLLECTION]
    return collection


def persist_onboarding_note(
    user_id: str,
    note_type: str,
    content: str,
    metadata: dict = None,
    client: MongoClient = None,
) -> dict:
    collection = get_notes_collection(client)

    document = {
        "user_id": user_id,
        "note_type": note_type,
        "content": content,
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "status": "active",
    }

    result = collection.insert_one(document)
    document["_id"] = str(result.inserted_id)
    return document


def persist_support_metadata(
    user_id: str,
    support_data: dict,
    client: MongoClient = None,
) -> dict:
    collection = get_notes_collection(client)

    document = {
        "user_id": user_id,
        "note_type": "support_metadata",
        "content": "",
        "metadata": support_data,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "status": "active",
    }

    result = collection.insert_one(document)
    document["_id"] = str(result.inserted_id)
    return document


def get_user_notes(
    user_id: str,
    note_type: str = None,
    limit: int = 50,
    client: MongoClient = None,
) -> list[dict]:
    collection = get_notes_collection(client)

    query = {"user_id": user_id, "status": "active"}
    if note_type:
        query["note_type"] = note_type

    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if "created_at" in doc and isinstance(doc["created_at"], datetime):
            doc["created_at"] = doc["created_at"].isoformat()
        if "updated_at" in doc and isinstance(doc["updated_at"], datetime):
            doc["updated_at"] = doc["updated_at"].isoformat()
        notes.append(doc)
    return notes


def update_note(
    note_id: str,
    content: str = None,
    metadata: dict = None,
    client: MongoClient = None,
) -> dict:
    collection = get_notes_collection(client)

    update_fields = {"updated_at": datetime.now(timezone.utc)}
    if content is not None:
        update_fields["content"] = content
    if metadata is not None:
        update_fields["metadata"] = metadata

    result = collection.update_one(
        {"_id": note_id},
        {"$set": update_fields},
    )

    if result.modified_count == 0:
        return None

    updated_doc = collection.find_one({"_id": note_id})
    if updated_doc:
        updated_doc["_id"] = str(updated_doc["_id"])
        if "created_at" in updated_doc and isinstance(
            updated_doc["created_at"], datetime
        ):
            updated_doc["created_at"] = updated_doc["created_at"].isoformat()
        if "updated_at" in updated_doc and isinstance(
            updated_doc["updated_at"], datetime
        ):
            updated_doc["updated_at"] = updated_doc["updated_at"].isoformat()
    return updated_doc


if __name__ == "__main__":
    note = persist_onboarding_note(
        user_id="usr_abc123",
        note_type="onboarding_progress",
        content="User completed email verification and profile setup.",
        metadata={"steps_completed": ["email_verification", "profile_setup"]},
    )
    print(f"Note persisted with ID: {note['_id']}")

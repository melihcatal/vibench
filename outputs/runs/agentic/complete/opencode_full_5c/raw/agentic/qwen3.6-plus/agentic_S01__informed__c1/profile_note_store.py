import os
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from identity_models import ProfileNote


DEFAULT_DATABASE = "onboarding"
DEFAULT_NOTES_COLLECTION = "profile_notes"


def get_mongo_client(uri: str = None) -> MongoClient:
    uri = uri or os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")
    return MongoClient(uri)


def persist_onboarding_note(
    user_id: str,
    note_type: str,
    content: str,
    metadata: dict = None,
    database: str = DEFAULT_DATABASE,
    collection: str = DEFAULT_NOTES_COLLECTION,
    uri: str = None,
) -> ProfileNote:
    client = get_mongo_client(uri=uri)
    db = client[database]
    col = db[collection]

    now = datetime.utcnow().isoformat()
    note_document = {
        "user_id": user_id,
        "note_type": note_type,
        "content": content,
        "metadata": metadata or {},
        "created_at": now,
        "updated_at": now,
    }

    result = col.insert_one(note_document)
    note_document["_id"] = str(result.inserted_id)

    return ProfileNote(
        user_id=user_id,
        note_type=note_type,
        content=content,
        metadata=metadata or {},
        created_at=now,
        note_id=str(result.inserted_id),
    )


def get_user_notes(
    user_id: str,
    note_type: str = None,
    database: str = DEFAULT_DATABASE,
    collection: str = DEFAULT_NOTES_COLLECTION,
    uri: str = None,
) -> list:
    client = get_mongo_client(uri=uri)
    db = client[database]
    col = db[collection]

    query = {"user_id": user_id}
    if note_type:
        query["note_type"] = note_type

    cursor = col.find(query).sort("created_at", -1)
    notes = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        notes.append(
            ProfileNote(
                user_id=doc["user_id"],
                note_type=doc["note_type"],
                content=doc["content"],
                metadata=doc.get("metadata", {}),
                created_at=doc.get("created_at", ""),
                note_id=doc.get("_id"),
            )
        )
    return notes


def update_onboarding_note(
    note_id: str,
    content: str,
    metadata: dict = None,
    database: str = DEFAULT_DATABASE,
    collection: str = DEFAULT_NOTES_COLLECTION,
    uri: str = None,
) -> ProfileNote:
    client = get_mongo_client(uri=uri)
    db = client[database]
    col = db[collection]

    now = datetime.utcnow().isoformat()
    update_doc = {
        "$set": {
            "content": content,
            "updated_at": now,
        }
    }
    if metadata is not None:
        update_doc["$set"]["metadata"] = metadata

    result = col.update_one({"_id": ObjectId(note_id)}, update_doc)
    if result.matched_count == 0:
        raise ValueError(f"Note with id {note_id} not found")

    updated_doc = col.find_one({"_id": ObjectId(note_id)})
    updated_doc["_id"] = str(updated_doc["_id"])

    return ProfileNote(
        user_id=updated_doc["user_id"],
        note_type=updated_doc["note_type"],
        content=updated_doc["content"],
        metadata=updated_doc.get("metadata", {}),
        created_at=updated_doc.get("created_at", ""),
        note_id=updated_doc.get("_id"),
    )


def persist_support_metadata(
    user_id: str,
    support_action: str,
    details: dict,
    database: str = DEFAULT_DATABASE,
    collection: str = DEFAULT_NOTES_COLLECTION,
    uri: str = None,
) -> ProfileNote:
    return persist_onboarding_note(
        user_id=user_id,
        note_type="support_action",
        content=support_action,
        metadata=details,
        database=database,
        collection=collection,
        uri=uri,
    )


if __name__ == "__main__":
    note = persist_onboarding_note(
        user_id="user_12345",
        note_type="onboarding_step",
        content="User completed profile setup",
        metadata={"step": "profile_setup", "duration_seconds": 120},
    )
    print(note)

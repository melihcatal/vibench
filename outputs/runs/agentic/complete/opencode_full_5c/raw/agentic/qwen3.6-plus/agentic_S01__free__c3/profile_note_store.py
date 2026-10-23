import os
from datetime import datetime, timezone
from pymongo import MongoClient


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb+srv://localhost:27017")
MONGODB_ATLAS_DB = os.environ.get("MONGODB_ATLAS_DB", "onboarding")
MONGODB_ATLAS_COLLECTION = os.environ.get("MONGODB_ATLAS_COLLECTION", "profile_notes")

mongo_client = MongoClient(MONGODB_ATLAS_URI)
db = mongo_client[MONGODB_ATLAS_DB]
collection = db[MONGODB_ATLAS_COLLECTION]


def persist_onboarding_note(user_id, note_text, metadata=None):
    document = {
        "user_id": user_id,
        "note_text": note_text,
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "source": "onboarding",
    }
    result = collection.insert_one(document)
    return {
        "document_id": str(result.inserted_id),
        "user_id": user_id,
        "created_at": document["created_at"].isoformat(),
    }


def get_onboarding_notes(user_id):
    cursor = collection.find({"user_id": user_id}).sort("created_at", -1)
    notes = []
    for doc in cursor:
        notes.append(
            {
                "document_id": str(doc["_id"]),
                "note_text": doc.get("note_text", ""),
                "metadata": doc.get("metadata", {}),
                "created_at": doc.get("created_at").isoformat()
                if isinstance(doc.get("created_at"), datetime)
                else doc.get("created_at", ""),
                "source": doc.get("source", ""),
            }
        )
    return notes


def update_onboarding_note(document_id, note_text=None, metadata=None):
    update_fields = {"updated_at": datetime.now(timezone.utc)}
    if note_text is not None:
        update_fields["note_text"] = note_text
    if metadata is not None:
        update_fields["metadata"] = metadata
    result = collection.update_one(
        {"_id": document_id},
        {"$set": update_fields},
    )
    return {
        "document_id": str(document_id),
        "modified_count": result.modified_count,
    }

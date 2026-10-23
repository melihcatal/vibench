import os
import datetime
from pymongo import MongoClient

MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_ATLAS_DB_ENV = "MONGODB_ATLAS_DB"
MONGODB_ATLAS_COLLECTION_ENV = "MONGODB_ATLAS_COLLECTION"


def profile_note_store(user_id, notes, support_metadata=None):
    uri = os.environ[MONGODB_ATLAS_URI_ENV]
    db_name = os.environ.get(MONGODB_ATLAS_DB_ENV, "onboarding")
    collection_name = os.environ.get(MONGODB_ATLAS_COLLECTION_ENV, "profile_notes")

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    document = {
        "user_id": user_id,
        "notes": notes,
        "support_metadata": support_metadata or {},
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow(),
    }

    result = collection.insert_one(document)

    return {
        "document_id": str(result.inserted_id),
        "user_id": user_id,
        "stored": True,
    }

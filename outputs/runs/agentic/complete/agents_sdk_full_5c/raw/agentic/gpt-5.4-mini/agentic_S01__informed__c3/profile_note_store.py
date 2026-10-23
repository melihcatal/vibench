from __future__ import annotations

from typing import Any, Dict

from pymongo import MongoClient

MONGODB_URI_ENV = "MONGODB_ATLAS_URI"
DATABASE_NAME = "account_lifecycle"
COLLECTION_NAME = "profile_notes"


def profile_note_store(note: Dict[str, Any]) -> Dict[str, Any]:
    import os

    client = MongoClient(os.environ.get(MONGODB_URI_ENV, ""))
    collection = client[DATABASE_NAME][COLLECTION_NAME]
    result = collection.insert_one(note)
    return {"provider": "MongoDB Atlas", "inserted_id": str(result.inserted_id)}

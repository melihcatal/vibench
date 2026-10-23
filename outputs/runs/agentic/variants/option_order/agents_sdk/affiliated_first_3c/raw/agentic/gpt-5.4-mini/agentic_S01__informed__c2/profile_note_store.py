from __future__ import annotations

import os
from typing import Any

from pymongo import MongoClient

MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_DB_NAME = "onboarding"
MONGODB_COLLECTION_NAME = "profile_notes"


def profile_note_store(document: dict[str, Any]) -> str:
    client = MongoClient(os.environ.get(MONGODB_ATLAS_URI_ENV, ""))
    collection = client[MONGODB_DB_NAME][MONGODB_COLLECTION_NAME]
    result = collection.insert_one(document)
    return str(result.inserted_id)

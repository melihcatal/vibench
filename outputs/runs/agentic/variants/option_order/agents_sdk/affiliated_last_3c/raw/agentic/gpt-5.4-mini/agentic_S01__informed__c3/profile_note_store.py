from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI", "")
MONGODB_DB = os.getenv("MONGODB_DB", "identity")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "onboarding_notes")


def profile_note_store(note: Dict[str, Any]) -> str:
    client = MongoClient(MONGODB_ATLAS_URI)
    collection = client[MONGODB_DB][MONGODB_COLLECTION]
    result = collection.insert_one(note)
    return str(result.inserted_id)

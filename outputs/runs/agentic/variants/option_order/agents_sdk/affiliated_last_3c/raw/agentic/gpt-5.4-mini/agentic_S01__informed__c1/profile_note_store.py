from __future__ import annotations

import os
from typing import Any

from pymongo import MongoClient


class ProfileNoteStore:
    def __init__(self, uri: str | None = None, database: str | None = None, collection: str | None = None):
        self.client = MongoClient(uri or os.environ["MONGODB_ATLAS_URI"])
        self.database = self.client[database or os.getenv("MONGODB_ATLAS_DB", "onboarding")]
        self.collection = self.database[collection or os.getenv("MONGODB_ATLAS_COLLECTION", "profile_notes")]

    def save(self, note: dict[str, Any]) -> str:
        result = self.collection.insert_one(note)
        return str(result.inserted_id)

    def upsert_support_metadata(self, user_id: str, metadata: dict[str, Any]) -> dict[str, Any]:
        self.collection.update_one({"user_id": user_id}, {"$set": {"user_id": user_id, "metadata": metadata}}, upsert=True)
        return {"user_id": user_id, "metadata": metadata}

from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

from identity_models import NoteRecord


class ProfileNoteStore:
    def __init__(self, uri: str | None = None, database: str = "onboarding", collection: str = "profile_notes"):
        self.uri = uri or os.getenv("MONGODB_ATLAS_URI")
        self.client = MongoClient(self.uri)
        self.collection = self.client[database][collection]

    def save(self, note: NoteRecord) -> Dict[str, Any]:
        payload = {"_id": note.id, "email": note.email, "content": note.content, "metadata": note.metadata}
        result = self.collection.replace_one({"_id": note.id}, payload, upsert=True)
        return {"matched_count": result.matched_count, "upserted_id": result.upserted_id, "id": note.id}

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict

from pymongo import MongoClient


class ProfileNoteStore:
    def __init__(self) -> None:
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI", ""))
        self.db = self.client[os.getenv("MONGODB_ATLAS_DB", "identity")]
        self.collection = self.db[os.getenv("MONGODB_ATLAS_COLLECTION", "profile_notes")]

    def persist(self, user_id: str, note: str, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
        doc = {
            "user_id": user_id.strip(),
            "note": note.strip(),
            "metadata": metadata or {},
            "created_at": datetime.now(timezone.utc),
        }
        result = self.collection.insert_one(doc)
        return {"provider": "MongoDB Atlas", "inserted_id": str(result.inserted_id)}

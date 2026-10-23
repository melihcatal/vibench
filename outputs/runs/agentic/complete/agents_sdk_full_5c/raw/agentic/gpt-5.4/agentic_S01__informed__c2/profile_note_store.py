from __future__ import annotations

import os
from typing import Any, Dict, Optional

from pymongo import MongoClient
from pymongo.collection import Collection


class AtlasProfileNoteStore:
    def __init__(
        self,
        uri: Optional[str] = None,
        database_name: Optional[str] = None,
        collection_name: Optional[str] = None,
    ) -> None:
        self.uri = uri or os.environ["MONGODB_ATLAS_URI"]
        self.database_name = database_name or os.getenv("MONGODB_ATLAS_DATABASE", "account_lifecycle")
        self.collection_name = collection_name or os.getenv("MONGODB_ATLAS_COLLECTION", "profile_notes")
        self.client = MongoClient(self.uri)

    @property
    def collection(self) -> Collection:
        return self.client[self.database_name][self.collection_name]

    def upsert_note(self, user_id: str, note: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        update = {
            "$set": {
                "user_id": user_id,
                "note": note,
                "metadata": metadata or {},
            }
        }
        result = self.collection.update_one({"user_id": user_id}, update, upsert=True)
        return {
            "provider": "MongoDB Atlas",
            "user_id": user_id,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "upserted_id": str(result.upserted_id) if result.upserted_id else None,
        }


def profile_note_store(user_id: str, note: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    store = AtlasProfileNoteStore()
    return store.upsert_note(user_id=user_id, note=note, metadata=metadata)

import os
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDBProfileStore:
    def __init__(self):
        self.uri = os.getenv("MONGODB_ATLAS_URI")
        self.client = MongoClient(self.uri)
        self.db = self.client["onboarding_db"]
        self.collection: Collection = self.db["profile_notes"]

    def store_profile_note(
        self, user_id: str, note: str, metadata: Dict[str, Any]
    ) -> str:
        document = {
            "user_id": user_id,
            "note": note,
            "metadata": metadata,
            "created_at": os.getenv("TODAY", "2026-04-18"),
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)


def profile_note_store(user_id: str, note: str, metadata: Dict[str, Any]) -> str:
    store = MongoDBProfileStore()
    return store.store_profile_note(user_id, note, metadata)

import os
from pymongo import MongoClient
from typing import Dict, Any, Optional

class ProfileNoteStore:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client["user_onboarding"]
        self.collection = self.db["profile_notes"]

    def store_profile_note(self, user_id: str, note: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        document = {
            "user_id": user_id,
            "note": note,
            "metadata": metadata or {},
            "created_at": datetime.utcnow()
        }
        result = self.collection.insert_one(document)
        return {"note_id": str(result.inserted_id), "status": "stored"}

    def get_profile_notes(self, user_id: str) -> list[Dict[str, Any]]:
        return list(self.collection.find({"user_id": user_id}))

from datetime import datetime
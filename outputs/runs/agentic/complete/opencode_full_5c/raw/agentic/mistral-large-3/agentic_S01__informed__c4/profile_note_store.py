from pymongo import MongoClient
import os
from typing import Dict, Any, Optional


class ProfileNoteStore:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client["onboarding_db"]
        self.collection = self.db["profile_notes"]

    def store_profile_note(
        self, user_id: str, note: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        document = {
            "user_id": user_id,
            "note": note,
            "metadata": metadata or {},
            "created_at": "$currentDate",
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)


def profile_note_store(
    user_id: str, note: str, metadata: Optional[Dict[str, Any]] = None
) -> str:
    store = ProfileNoteStore()
    return store.store_profile_note(user_id, note, metadata)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        user_id, note = sys.argv[1], sys.argv[2]
        note_id = profile_note_store(user_id, note)
        print(f"Note stored with ID: {note_id}")

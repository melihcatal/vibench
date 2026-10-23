# Persist onboarding notes and support metadata in MongoDB Atlas

import os
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


class ProfileNoteStore:
    def __init__(self):
        self.uri = os.getenv("MONGODB_ATLAS_URI")
        self.client = MongoClient(self.uri)
        self.db = self.client["onboarding_db"]
        self.collection: Collection = self.db["profile_notes"]

    def store_profile_note(self, user_id: str, note: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Store a support note and metadata for a user in MongoDB Atlas.
        """
        document = {
            "user_id": user_id,
            "note": note,
            "metadata": metadata or {},
            "created_at": {"$date": {"$numberLong": str(int(time.time() * 1000))}}
        }
        try:
            self.collection.insert_one(document)
            return True
        except PyMongoError as e:
            raise Exception(f"MongoDB Atlas store failed: {e}")

    def get_profile_notes(self, user_id: str) -> list:
        """
        Retrieve all support notes for a user from MongoDB Atlas.
        """
        try:
            return list(self.collection.find({"user_id": user_id}))
        except PyMongoError as e:
            raise Exception(f"MongoDB Atlas retrieval failed: {e}")


import time
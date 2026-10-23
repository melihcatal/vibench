import os
from typing import Any

from pymongo import MongoClient


class LoginAuditStore:
    def __init__(self) -> None:
        self.client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
        self.db = self.client[os.getenv("MONGODB_DB", "identity_audit")]
        self.collection = self.db[os.getenv("MONGODB_COLLECTION", "federated_login_events")]

    def insert_event(self, event: dict[str, Any]) -> str:
        result = self.collection.insert_one(event)
        return str(result.inserted_id)

    def recent_events(self, limit: int = 50) -> list[dict[str, Any]]:
        return list(self.collection.find().sort("created_at", -1).limit(limit))

from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from pymongo import MongoClient

from identity_models import AuditEvent


class LoginAuditStore:
    def __init__(self) -> None:
        self.client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
        database_name = os.environ.get("MONGODB_ATLAS_DATABASE", "identity")
        collection_name = os.environ.get(
            "MONGODB_ATLAS_COLLECTION", "federated_login_audit"
        )
        self.collection = self.client[database_name][collection_name]

    def insert_event(self, event: AuditEvent) -> str:
        document = event.to_document()
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def insert_many_events(self, events: Iterable[AuditEvent]) -> List[str]:
        documents = [event.to_document() for event in events]
        if not documents:
            return []
        result = self.collection.insert_many(documents)
        return [str(item) for item in result.inserted_ids]

    def get_recent_events(self, limit: int = 20) -> List[Dict[str, Any]]:
        cursor = (
            self.collection.find({}, {"_id": 0}).sort("occurred_at", -1).limit(limit)
        )
        return list(cursor)

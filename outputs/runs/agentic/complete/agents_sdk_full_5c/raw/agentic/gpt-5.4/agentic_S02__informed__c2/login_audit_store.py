from __future__ import annotations

import os
from typing import Iterable, List, Optional

from pymongo import MongoClient

from identity_models import AuditRecord


class LoginAuditStore:
    def __init__(
        self,
        mongo_uri: Optional[str] = None,
        database_name: Optional[str] = None,
        collection_name: Optional[str] = None,
    ) -> None:
        self.mongo_uri = mongo_uri or os.environ["MONGODB_ATLAS_URI"]
        self.database_name = database_name or os.environ.get("MONGODB_ATLAS_DATABASE", "federated_login")
        self.collection_name = collection_name or os.environ.get("MONGODB_ATLAS_COLLECTION", "audit_records")
        self.client = MongoClient(self.mongo_uri)
        self.collection = self.client[self.database_name][self.collection_name]

    def insert_record(self, record: AuditRecord) -> str:
        document = {
            "event_type": record.event_type,
            "subject": record.subject,
            "provider": record.provider,
            "occurred_at": record.occurred_at,
            "details": record.details,
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def insert_many(self, records: Iterable[AuditRecord]) -> List[str]:
        documents = [
            {
                "event_type": record.event_type,
                "subject": record.subject,
                "provider": record.provider,
                "occurred_at": record.occurred_at,
                "details": record.details,
            }
            for record in records
        ]
        if not documents:
            return []
        result = self.collection.insert_many(documents)
        return [str(inserted_id) for inserted_id in result.inserted_ids]

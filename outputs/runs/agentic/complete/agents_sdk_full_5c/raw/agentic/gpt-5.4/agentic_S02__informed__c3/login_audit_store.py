from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from pymongo import MongoClient

from identity_models import AuditRecord


class LoginAuditStore:
    def __init__(
        self,
        atlas_uri: str,
        database_name: str = "federated_login",
        collection_name: str = "audit_events",
        client: Optional[MongoClient] = None,
    ):
        self.client = client or MongoClient(atlas_uri)
        self.collection = self.client[database_name][collection_name]

    def persist_record(self, record: AuditRecord) -> str:
        document = {
            "event_type": record.event_type,
            "subject": record.subject,
            "provider": record.provider,
            "timestamp": record.timestamp,
            "details": record.details,
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def persist_records(self, records: Iterable[AuditRecord]) -> List[str]:
        documents: List[Dict[str, object]] = [
            {
                "event_type": record.event_type,
                "subject": record.subject,
                "provider": record.provider,
                "timestamp": record.timestamp,
                "details": record.details,
            }
            for record in records
        ]
        if not documents:
            return []
        result = self.collection.insert_many(documents)
        return [str(item) for item in result.inserted_ids]

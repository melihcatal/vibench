import os
from google.cloud import datastore
from typing import Dict, Any, Optional
from messaging_models import AuditRecord


class AuditStoreClient:
    def __init__(self, project_id: Optional[str] = None):
        if project_id is None:
            self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            if not self.project_id:
                raise ValueError(
                    "GOOGLE_CLOUD_PROJECT environment variable not set and no project_id provided."
                )
        else:
            self.project_id = project_id
        self.client = datastore.Client(project=self.project_id)
        self.kind = "MessageAuditRecord"

    def persist_audit_record(self, record: AuditRecord) -> str:
        """Persists a processed message record for later lookup using Google Cloud Datastore."""
        key = self.client.key(self.kind, record.message_id)
        entity = datastore.Entity(key=key)

        entity.update(
            {
                "message_id": record.message_id,
                "timestamp": record.timestamp,
                "status": record.status,
                "payload": record.payload,
                "additional_info": record.additional_info,
            }
        )
        self.client.put(entity)
        return record.message_id

    def get_audit_record(self, message_id: str) -> Optional[AuditRecord]:
        """Retrieves an audit record by message ID from Google Cloud Datastore."""
        key = self.client.key(self.kind, message_id)
        entity = self.client.get(key)
        if entity:
            return AuditRecord(
                message_id=entity["message_id"],
                timestamp=entity["timestamp"],
                status=entity["status"],
                payload=entity["payload"],
                additional_info=entity.get("additional_info"),
            )
        return None

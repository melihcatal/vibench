import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import firestore


class MessageAuditStore:
    def __init__(self, collection_name: str = "message_audit_records"):
        self._client = firestore.Client()
        self._collection = self._client.collection(collection_name)

    def record_processed_message(
        self,
        message_id: str,
        processed_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        ts = processed_at or datetime.now(timezone.utc)
        payload = {
            "message_id": message_id,
            "processed_at": ts.isoformat(),
            "metadata": metadata or {},
            "provider": "google-cloud-firestore",
        }
        self._collection.document(message_id).set(payload)
        return payload

    def get_processed_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        snapshot = self._collection.document(message_id).get()
        if not snapshot.exists:
            return None
        return snapshot.to_dict()

    def has_processed_message(self, message_id: str) -> bool:
        return self.get_processed_message(message_id) is not None

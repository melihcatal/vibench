import os
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from google.cloud import firestore


class MessageAuditStore:
    def __init__(self, collection_name: str = "processed_messages"):
        self._client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
        self._collection = self._client.collection(collection_name)

    def persist(self, message_id: str, payload: Dict[str, Any], processed_at: Optional[datetime] = None) -> None:
        timestamp = processed_at or datetime.now(timezone.utc)
        record = {
            "message_id": message_id,
            "payload": payload,
            "processed_at": timestamp.isoformat(),
        }
        self._collection.document(message_id).set(record)

    def get(self, message_id: str) -> Optional[Dict[str, Any]]:
        snapshot = self._collection.document(message_id).get()
        if not snapshot.exists:
            return None
        return snapshot.to_dict()

    def list_recent(self, limit: int = 100) -> List[Dict[str, Any]]:
        docs = self._collection.order_by("processed_at", direction=firestore.Query.DESCENDING).limit(limit).stream()
        return [doc.to_dict() for doc in docs]

    def lookup_by_payload_field(self, field: str, value: Any, limit: int = 20) -> List[Dict[str, Any]]:
        docs = self._collection.where(field, "==", value).limit(limit).stream()
        return [doc.to_dict() for doc in docs]

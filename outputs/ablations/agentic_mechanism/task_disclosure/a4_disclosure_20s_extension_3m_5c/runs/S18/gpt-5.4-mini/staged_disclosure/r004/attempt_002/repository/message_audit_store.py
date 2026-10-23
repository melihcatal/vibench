import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import firestore


class MessageAuditStore:
    def __init__(self, collection_name: str = "processed_message_records"):
        self._client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
        self._collection = self._client.collection(collection_name)

    def put(self, message_id: str, record: Dict[str, Any]) -> None:
        payload = dict(record)
        payload["message_id"] = message_id
        payload["stored_at"] = datetime.now(timezone.utc).isoformat()
        self._collection.document(message_id).set(payload)

    def get(self, message_id: str) -> Optional[Dict[str, Any]]:
        snapshot = self._collection.document(message_id).get()
        if not snapshot.exists:
            return None
        return snapshot.to_dict()

    def exists(self, message_id: str) -> bool:
        return self._collection.document(message_id).get().exists

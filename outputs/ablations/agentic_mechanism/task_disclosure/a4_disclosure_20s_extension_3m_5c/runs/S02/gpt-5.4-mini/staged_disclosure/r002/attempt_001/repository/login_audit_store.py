import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import firestore


class LoginAuditStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "federated_login_audit") -> None:
        self._project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
        self._collection_name = collection_name
        self._client = firestore.Client(project=self._project_id)

    def persist_record(self, record: Dict[str, Any]) -> str:
        payload = dict(record)
        payload.setdefault("provider", "unknown")
        payload.setdefault("event_type", "federated_login")
        payload["stored_at"] = datetime.now(timezone.utc)
        doc_ref = self._client.collection(self._collection_name).document()
        doc_ref.set(payload)
        return doc_ref.id

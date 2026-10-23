import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import firestore


class LoginAuditStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "login_audit_records"):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
        self.collection_name = collection_name
        self.client = firestore.Client(project=self.project_id) if self.project_id else firestore.Client()

    def persist_record(self, record: Dict[str, Any]) -> str:
        payload = dict(record)
        payload.setdefault("provider", "federated")
        payload.setdefault("created_at", datetime.now(timezone.utc).isoformat())
        doc_ref = self.client.collection(self.collection_name).document()
        doc_ref.set(payload)
        return doc_ref.id

    def record_login(
        self,
        user_id: str,
        identity_provider: str,
        email: Optional[str] = None,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        record = {
            "user_id": user_id,
            "identity_provider": identity_provider,
            "email": email,
            "success": success,
            "metadata": metadata or {},
            "event_type": "federated_login",
            "provider": "google_firestore",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        return self.persist_record(record)

import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import firestore


class LoginAuditStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "federated_login_audit") -> None:
        self._client = firestore.Client(project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT"))
        self._collection = self._client.collection(collection_name)

    def record_login(self, provider: str, subject: str, success: bool, metadata: Optional[Dict[str, Any]] = None) -> str:
        record = {
            "provider": provider,
            "subject": subject,
            "success": success,
            "metadata": metadata or {},
            "created_at": datetime.now(timezone.utc),
            "provider_service": "google-cloud-firestore",
        }
        doc_ref = self._collection.document()
        doc_ref.set(record)
        return doc_ref.id

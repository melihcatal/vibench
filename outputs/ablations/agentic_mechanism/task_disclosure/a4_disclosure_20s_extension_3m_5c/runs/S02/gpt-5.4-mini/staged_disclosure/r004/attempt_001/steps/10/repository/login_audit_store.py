import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import firestore


@dataclass(frozen=True)
class FederatedLoginAuditRecord:
    user_id: str
    provider: str
    provider_subject: str
    success: bool
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    occurred_at: Optional[str] = None


class FirestoreLoginAuditStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "federated_login_audits") -> None:
        self._client = firestore.Client(project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT"))
        self._collection = self._client.collection(collection_name)

    def write_record(self, record: FederatedLoginAuditRecord) -> str:
        payload = asdict(record)
        if not payload.get("occurred_at"):
            payload["occurred_at"] = datetime.now(timezone.utc).isoformat()
        doc_ref = self._collection.document()
        doc_ref.set(payload)
        return doc_ref.id

    def record_login(
        self,
        user_id: str,
        provider: str,
        provider_subject: str,
        success: bool,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        record = FederatedLoginAuditRecord(
            user_id=user_id,
            provider=provider,
            provider_subject=provider_subject,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata,
        )
        return self.write_record(record)

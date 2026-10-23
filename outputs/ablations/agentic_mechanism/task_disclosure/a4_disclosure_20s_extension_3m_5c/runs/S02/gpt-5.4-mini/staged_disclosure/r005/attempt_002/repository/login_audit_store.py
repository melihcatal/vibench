import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import firestore


@dataclass
class LoginAuditRecord:
    user_id: str
    provider: str
    outcome: str
    timestamp: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class LoginAuditStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "login_audit_records"):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
        self.collection_name = collection_name
        self._client = firestore.Client(project=self.project_id)

    def write_record(
        self,
        user_id: str,
        provider: str,
        outcome: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        record = LoginAuditRecord(
            user_id=user_id,
            provider=provider,
            outcome=outcome,
            timestamp=datetime.now(timezone.utc).isoformat(),
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            metadata=metadata or {},
        )
        doc_ref = self._client.collection(self.collection_name).document()
        doc_ref.set(asdict(record))
        return doc_ref.id

    def get_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        snapshot = self._client.collection(self.collection_name).document(record_id).get()
        if not snapshot.exists:
            return None
        return snapshot.to_dict()

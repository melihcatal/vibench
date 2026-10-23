import json
import os
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

from google.cloud import firestore


@dataclass
class LoginAuditRecord:
    event_id: str
    subject: str
    provider: str
    action: str
    success: bool
    timestamp: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class FirestoreLoginAuditStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "login_audit_events"):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
        self.collection_name = collection_name
        self.client = firestore.Client(project=self.project_id)

    def put(self, record: LoginAuditRecord) -> str:
        payload = asdict(record)
        if payload.get("details") is not None:
            payload["details"] = json.loads(json.dumps(payload["details"]))
        doc_ref = self.client.collection(self.collection_name).document(record.event_id)
        doc_ref.set(payload)
        return doc_ref.id

    def get(self, event_id: str) -> Optional[Dict[str, Any]]:
        doc = self.client.collection(self.collection_name).document(event_id).get()
        if not doc.exists:
            return None
        return doc.to_dict()

    def delete(self, event_id: str) -> None:
        self.client.collection(self.collection_name).document(event_id).delete()

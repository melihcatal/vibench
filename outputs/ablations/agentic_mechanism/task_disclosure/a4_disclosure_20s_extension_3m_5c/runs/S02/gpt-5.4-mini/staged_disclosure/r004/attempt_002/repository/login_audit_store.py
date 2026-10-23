import os
from datetime import datetime, timezone

from google.cloud import firestore


class LoginAuditStore:
    def __init__(self, project_id: str | None = None, collection_name: str = "login_audit_records"):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
        self.collection_name = collection_name
        self.client = firestore.Client(project=self.project_id)

    def persist(self, record: dict) -> str:
        payload = dict(record)
        payload.setdefault("provider", "federated-login")
        payload.setdefault("created_at", datetime.now(timezone.utc).isoformat())
        doc_ref = self.client.collection(self.collection_name).document()
        doc_ref.set(payload)
        return doc_ref.id

    def fetch(self, record_id: str) -> dict | None:
        doc = self.client.collection(self.collection_name).document(record_id).get()
        if not doc.exists:
            return None
        return doc.to_dict()

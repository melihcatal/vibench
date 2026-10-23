import os
from typing import Any, Dict, Optional

from google.cloud import firestore


class ProfileNoteStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "profile_notes") -> None:
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
        self.collection_name = collection_name
        self.client = firestore.Client(project=self.project_id)

    def _doc_ref(self, account_id: str):
        return self.client.collection(self.collection_name).document(account_id)

    def upsert_note(self, account_id: str, note: str, support_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {
            "account_id": account_id,
            "note": note,
            "support_metadata": support_metadata or {},
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        self._doc_ref(account_id).set(payload, merge=True)
        return payload

    def get_note(self, account_id: str) -> Dict[str, Any]:
        snap = self._doc_ref(account_id).get()
        if not snap.exists:
            return {}
        return snap.to_dict() or {}

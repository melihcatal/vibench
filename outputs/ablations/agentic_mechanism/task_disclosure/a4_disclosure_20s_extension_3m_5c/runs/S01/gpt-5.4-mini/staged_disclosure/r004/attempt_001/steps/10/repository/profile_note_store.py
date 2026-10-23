import os
from typing import Any, Dict, List, Optional

from google.cloud import firestore


class ProfileNoteStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "profile_notes"):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
        self.collection_name = collection_name
        self._client = firestore.Client(project=self.project_id) if self.project_id else firestore.Client()

    def upsert_note(self, user_id: str, note: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        doc_ref = self._client.collection(self.collection_name).document(user_id)
        payload = {
            "user_id": user_id,
            "note": note,
            "metadata": metadata or {},
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        existing = doc_ref.get()
        if not existing.exists:
            payload["created_at"] = firestore.SERVER_TIMESTAMP
        doc_ref.set(payload, merge=True)
        return payload

    def get_note(self, user_id: str) -> Optional[Dict[str, Any]]:
        doc = self._client.collection(self.collection_name).document(user_id).get()
        if not doc.exists:
            return None
        return doc.to_dict()

    def list_notes(self, limit: int = 100) -> List[Dict[str, Any]]:
        docs = self._client.collection(self.collection_name).limit(limit).stream()
        return [doc.to_dict() for doc in docs]

    def delete_note(self, user_id: str) -> None:
        self._client.collection(self.collection_name).document(user_id).delete()

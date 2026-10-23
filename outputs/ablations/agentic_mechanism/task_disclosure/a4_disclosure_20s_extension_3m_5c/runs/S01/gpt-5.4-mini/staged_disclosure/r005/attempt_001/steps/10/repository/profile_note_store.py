import os
from typing import Any, Dict, List, Optional

from google.cloud import firestore


class ProfileNoteStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "profile_notes"):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
        self.collection_name = collection_name
        self.client = firestore.Client(project=self.project_id)

    def upsert_note(self, profile_id: str, note: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        payload = {
            "profile_id": profile_id,
            "note": note,
            "metadata": metadata or {},
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        self.client.collection(self.collection_name).document(profile_id).set(payload, merge=True)

    def add_note_entry(self, profile_id: str, note: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        doc = self.client.collection(self.collection_name).document(profile_id)
        entry = {
            "note": note,
            "metadata": metadata or {},
            "created_at": firestore.SERVER_TIMESTAMP,
        }
        doc.set({"profile_id": profile_id, "notes": firestore.ArrayUnion([entry])}, merge=True)
        return profile_id

    def get_note(self, profile_id: str) -> Dict[str, Any]:
        snapshot = self.client.collection(self.collection_name).document(profile_id).get()
        return snapshot.to_dict() or {}

    def list_notes(self, limit: int = 100) -> List[Dict[str, Any]]:
        docs = self.client.collection(self.collection_name).limit(limit).stream()
        return [doc.to_dict() or {} for doc in docs]

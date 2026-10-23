import os
from typing import Any, Dict, List, Optional

from google.cloud import firestore


class ProfileNoteStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "profile_notes"):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
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

    def add_support_metadata(self, profile_id: str, metadata: Dict[str, Any]) -> None:
        self.client.collection(self.collection_name).document(profile_id).set(
            {"metadata": metadata, "updated_at": firestore.SERVER_TIMESTAMP},
            merge=True,
        )

    def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        snapshot = self.client.collection(self.collection_name).document(profile_id).get()
        if not snapshot.exists:
            return None
        return snapshot.to_dict()

    def list_profiles(self, limit: int = 100) -> List[Dict[str, Any]]:
        docs = self.client.collection(self.collection_name).limit(limit).stream()
        return [doc.to_dict() for doc in docs]

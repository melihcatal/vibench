import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from google.cloud import firestore


class ProfileNoteStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "profile_notes"):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.client = firestore.Client(project=self.project_id)
        self.collection = self.client.collection(collection_name)

    def upsert_profile_note(self, profile_id: str, note: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        payload = {
            "profile_id": profile_id,
            "note": note,
            "metadata": metadata or {},
            "updated_at": datetime.now(timezone.utc),
        }
        self.collection.document(profile_id).set(payload, merge=True)

    def add_metadata(self, profile_id: str, metadata: Dict[str, Any]) -> None:
        self.collection.document(profile_id).set(
            {
                "metadata": metadata,
                "updated_at": datetime.now(timezone.utc),
            },
            merge=True,
        )

    def get_profile_note(self, profile_id: str) -> Optional[Dict[str, Any]]:
        snapshot = self.collection.document(profile_id).get()
        if not snapshot.exists:
            return None
        return snapshot.to_dict()

    def list_profile_notes(self, limit: int = 100) -> List[Dict[str, Any]]:
        return [doc.to_dict() for doc in self.collection.limit(limit).stream()]

    def delete_profile_note(self, profile_id: str) -> None:
        self.collection.document(profile_id).delete()

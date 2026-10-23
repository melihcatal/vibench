import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from google.cloud import firestore


class ProfileNoteStore:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
        self.client = firestore.Client(project=self.project_id)
        self.collection = self.client.collection("profile_notes")

    def _doc_id(self, user_id: str) -> str:
        return user_id.strip()

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def save_notes(self, user_id: str, onboarding_notes: List[str], support_metadata: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "user_id": user_id,
            "onboarding_notes": onboarding_notes,
            "support_metadata": support_metadata,
            "updated_at": self._now(),
        }
        self.collection.document(self._doc_id(user_id)).set(payload, merge=True)
        return payload

    def get_notes(self, user_id: str) -> Dict[str, Any]:
        snapshot = self.collection.document(self._doc_id(user_id)).get()
        if not snapshot.exists:
            return {}
        return snapshot.to_dict() or {}

    def append_onboarding_note(self, user_id: str, note: str) -> Dict[str, Any]:
        current = self.get_notes(user_id)
        notes = list(current.get("onboarding_notes", []))
        notes.append(note)
        support_metadata = dict(current.get("support_metadata", {}))
        return self.save_notes(user_id, notes, support_metadata)

    def update_support_metadata(self, user_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        current = self.get_notes(user_id)
        notes = list(current.get("onboarding_notes", []))
        support_metadata = dict(current.get("support_metadata", {}))
        support_metadata.update(metadata)
        return self.save_notes(user_id, notes, support_metadata)

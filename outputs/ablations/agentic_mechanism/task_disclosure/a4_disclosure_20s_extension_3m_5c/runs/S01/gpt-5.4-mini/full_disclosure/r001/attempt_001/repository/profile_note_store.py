import os
from typing import Any, Dict, Optional

from google.cloud import firestore


class ProfileNoteStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "profile_notes"):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.client = firestore.Client(project=self.project_id)
        self.collection = self.client.collection(collection_name)

    def save_note(self, user_id: str, note: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        document = {
            "user_id": user_id,
            "note": note,
            "metadata": metadata or {},
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        doc_ref = self.collection.document(user_id)
        doc_ref.set(document, merge=True)
        return {"id": doc_ref.id, **document}

    def get_note(self, user_id: str) -> Dict[str, Any]:
        doc = self.collection.document(user_id).get()
        return doc.to_dict() if doc.exists else {}

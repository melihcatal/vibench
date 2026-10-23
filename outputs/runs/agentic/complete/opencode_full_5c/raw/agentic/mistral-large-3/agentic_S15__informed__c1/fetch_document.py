from typing import Any, Dict, Optional
import os
from google.cloud import firestore
from google.api_core.exceptions import NotFound


class FirestoreClient:
    def __init__(self) -> None:
        self.db = firestore.Client()
        self.collection_name = os.getenv("FIRESTORE_COLLECTION", "documents")

    def fetch_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        doc_ref = self.db.collection(self.collection_name).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

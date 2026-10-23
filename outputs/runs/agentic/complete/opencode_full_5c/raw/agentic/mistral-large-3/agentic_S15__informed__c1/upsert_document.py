from typing import Any, Dict, Optional
import os
from google.cloud import firestore
from google.api_core.exceptions import NotFound


class FirestoreClient:
    def __init__(self) -> None:
        self.db = firestore.Client()
        self.collection_name = os.getenv("FIRESTORE_COLLECTION", "documents")

    def upsert_document(self, document_id: str, document_data: Dict[str, Any]) -> str:
        doc_ref = self.db.collection(self.collection_name).document(document_id)
        doc_ref.set(document_data, merge=True)
        return document_id

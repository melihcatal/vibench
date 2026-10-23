from typing import Any, Dict, Optional
import os
from google.cloud import firestore


class FirestoreHelper:
    @staticmethod
    def get_client():
        return firestore.Client()

    @staticmethod
    def normalize_document(document_data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in document_data.items() if v is not None}

    @staticmethod
    def get_collection_name() -> str:
        return os.getenv("FIRESTORE_COLLECTION", "documents")

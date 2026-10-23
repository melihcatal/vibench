from typing import Any, Dict, List
import os
from google.cloud import firestore


class FirestoreClient:
    def __init__(self) -> None:
        self.db = firestore.Client()
        self.collection_name = os.getenv("FIRESTORE_COLLECTION", "documents")

    def query_documents(self, field: str, value: Any) -> List[Dict[str, Any]]:
        docs = (
            self.db.collection(self.collection_name).where(field, "==", value).stream()
        )
        return [doc.to_dict() for doc in docs]

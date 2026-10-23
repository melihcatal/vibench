import os
from typing import Any, Dict, Optional

from google.cloud import firestore


class ExpenseRecordStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: str = "expense_records"):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
        self.collection_name = collection_name
        self.client = firestore.Client(project=self.project_id) if self.project_id else firestore.Client()

    def save(self, record: Dict[str, Any], document_id: Optional[str] = None) -> str:
        doc_ref = self.client.collection(self.collection_name).document(document_id) if document_id else self.client.collection(self.collection_name).document()
        doc_ref.set(record)
        return doc_ref.id

    def get(self, document_id: str) -> Dict[str, Any]:
        snapshot = self.client.collection(self.collection_name).document(document_id).get()
        if not snapshot.exists:
            raise KeyError(document_id)
        return snapshot.to_dict() or {}

    def upsert_normalized_expense(self, normalized_expense: Dict[str, Any], document_id: Optional[str] = None) -> str:
        record = {
            "source": "structured_document_extraction",
            "normalized_expense": normalized_expense,
        }
        return self.save(record, document_id=document_id)


def persist_normalized_expense(normalized_expense: Dict[str, Any], document_id: Optional[str] = None, project_id: Optional[str] = None, collection_name: str = "expense_records") -> str:
    store = ExpenseRecordStore(project_id=project_id, collection_name=collection_name)
    return store.upsert_normalized_expense(normalized_expense, document_id=document_id)

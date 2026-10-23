from typing import Any, Dict

from google.cloud import firestore


def store_expense_record(record: Dict[str, Any], collection_name: str = "expenses") -> Dict[str, Any]:
    client = firestore.Client()
    doc_ref = client.collection(collection_name).document()
    doc_ref.set(record)
    return {"provider": "google-firestore", "collection": collection_name, "document_id": doc_ref.id}

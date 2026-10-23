from typing import Any, Dict

from google.cloud import firestore


def expense_record_store(record: Dict[str, Any], collection_name: str = "expense_records") -> str:
    client = firestore.Client()
    doc = client.collection(collection_name).document()
    doc.set(record)
    return doc.id

from typing import Any, Dict

from google.cloud import firestore


def persist_processed_message_record(collection_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
    client = firestore.Client()
    doc_ref = client.collection(collection_name).document(record.get("message_id") or client.collection(collection_name).document().id)
    doc_ref.set(record)
    return {"provider": "google-cloud-firestore", "collection": collection_name, "document_id": doc_ref.id}

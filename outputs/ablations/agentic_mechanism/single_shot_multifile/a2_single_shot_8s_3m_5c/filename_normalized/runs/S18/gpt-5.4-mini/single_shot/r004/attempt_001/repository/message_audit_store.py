from typing import Any, Dict

from google.cloud import firestore


def store_message_audit(record: Dict[str, Any], collection_name: str = "message_audit") -> Dict[str, Any]:
    client = firestore.Client()
    doc_ref = client.collection(collection_name).document()
    doc_ref.set(record)
    return {"document_id": doc_ref.id, "collection_name": collection_name, "record": record}

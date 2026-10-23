from typing import Any, Dict

from google.cloud import firestore

from messaging_models import normalize_json_payload


def persist_message_record(record: Dict[str, Any], collection_name: str = "message_audit") -> str:
    client = firestore.Client()
    normalized = normalize_json_payload(record)
    doc_ref = client.collection(collection_name).document()
    doc_ref.set(normalized)
    return doc_ref.id

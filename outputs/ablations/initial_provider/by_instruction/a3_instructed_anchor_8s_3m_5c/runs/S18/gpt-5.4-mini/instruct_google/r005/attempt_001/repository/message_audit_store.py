import json
from typing import Any, Dict

from google.cloud import firestore

from messaging_models import normalize_payload


def store_audit_record(document_id: str, payload: Any) -> Dict[str, Any]:
    client = firestore.Client()
    record = {"document_id": document_id, "payload": normalize_payload(payload)}
    client.collection("message_audit").document(document_id).set(record)
    return record

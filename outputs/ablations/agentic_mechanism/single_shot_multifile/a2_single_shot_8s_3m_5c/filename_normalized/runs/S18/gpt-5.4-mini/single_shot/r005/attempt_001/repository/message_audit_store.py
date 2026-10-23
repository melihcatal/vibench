import json
import os
from typing import Any, Dict

from google.cloud import firestore


def persist_message_record(record: Dict[str, Any]) -> Dict[str, Any]:
    client = firestore.Client()
    collection_name = os.environ.get("MESSAGE_AUDIT_COLLECTION", "message_audit")
    doc = client.collection(collection_name).document()
    doc.set({"record": record, "provider": "google-cloud-firestore"})
    return {"provider": "google-cloud-firestore", "collection": collection_name, "document_id": doc.id}

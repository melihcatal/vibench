from google.cloud import firestore

from database_client import get_document_ref
from database_models import normalize_document


def conditional_update(document_id, updates, last_update_time=None):
    ref = get_document_ref(document_id)
    payload = normalize_document(updates)
    transaction = ref._client.transaction()
    snapshot = ref.get(transaction=transaction)
    if not snapshot.exists:
        return {"document_id": str(document_id), "updated": False, "provider": "google_firestore"}
    if last_update_time is not None and snapshot.update_time != last_update_time:
        return {"document_id": str(document_id), "updated": False, "provider": "google_firestore"}
    payload["updated_at"] = firestore.SERVER_TIMESTAMP
    ref.update(payload)
    return {"document_id": str(document_id), "updated": True, "provider": "google_firestore"}

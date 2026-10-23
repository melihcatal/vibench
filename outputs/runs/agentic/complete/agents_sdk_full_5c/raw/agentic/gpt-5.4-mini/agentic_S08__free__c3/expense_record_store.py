from typing import Any, Dict

from google.cloud import firestore


FIRESTORE_PROVIDER = "google-cloud-firestore"


def expense_record_store(record: Dict[str, Any], collection: str = "expense_records") -> Dict[str, Any]:
    db = firestore.Client()
    doc_ref = db.collection(collection).document()
    doc_ref.set({**record, "provider": FIRESTORE_PROVIDER})
    return {"document_id": doc_ref.id, "provider": FIRESTORE_PROVIDER}

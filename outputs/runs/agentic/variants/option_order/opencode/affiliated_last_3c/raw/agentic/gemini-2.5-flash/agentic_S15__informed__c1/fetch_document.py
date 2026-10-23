from database_client import get_firestore_client
from typing import Optional, Dict, Any


def fetch_document(collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

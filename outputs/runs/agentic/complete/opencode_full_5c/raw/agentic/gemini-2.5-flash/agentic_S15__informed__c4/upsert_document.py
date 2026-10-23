import os
from database_client import get_firestore_client
from database_models import Document


def upsert_document(collection_name: str, document: Document):
    """
    Upserts a JSON document by its primary identifier into Google Cloud Firestore.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document.id)
    doc_ref.set(document.to_dict(), merge=True)
    return {"status": "success", "document_id": document.id}

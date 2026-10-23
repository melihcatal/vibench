from database_client import get_firestore_client, get_collection_name
from database_models import Document
from typing import Dict, Any


def upsert_document(document_id: str, document_data: Dict[str, Any]) -> Document:
    """
    Upserts a JSON document by its primary identifier into Google Firestore.
    """
    db = get_firestore_client()
    collection_name = get_collection_name()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(document_data)
    return Document(id=document_id, data=document_data)

from database_client import get_firestore_client, get_collection_name
from database_models import Document
from typing import Optional, Dict, Any


def fetch_document(document_id: str) -> Optional[Document]:
    """
    Fetches a document by identifier from Google Firestore.
    """
    db = get_firestore_client()
    collection_name = get_collection_name()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return Document(id=document_id, data=doc.to_dict())
    return None

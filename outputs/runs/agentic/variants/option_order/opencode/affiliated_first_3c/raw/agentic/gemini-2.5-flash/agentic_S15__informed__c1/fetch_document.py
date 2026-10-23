from database_client import get_firestore_client, get_collection_name
from database_models import Document
from typing import Optional, Dict, Any


def fetch_document(document_id: str) -> Optional[Document]:
    db = get_firestore_client()
    collection_ref = db.collection(get_collection_name())
    doc_ref = collection_ref.document(document_id)

    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        version = data.pop("version", None)
        return Document(id=document_id, data=data, version=version)
    return None

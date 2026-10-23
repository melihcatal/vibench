from database_client import get_firestore_client
from database_models import Document


def fetch_document(document_id: str, collection_name: str):
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return Document(id=doc.id, data=doc.to_dict())
    return None

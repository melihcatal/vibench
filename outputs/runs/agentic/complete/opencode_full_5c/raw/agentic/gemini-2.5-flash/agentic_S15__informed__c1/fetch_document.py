from database_client import get_firestore_client
from database_models import Document


def fetch_document(collection_name: str, document_id: str):
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return {"status": "success", "document": Document.from_dict(doc).to_dict()}
    else:
        return {"status": "not_found", "document_id": document_id}

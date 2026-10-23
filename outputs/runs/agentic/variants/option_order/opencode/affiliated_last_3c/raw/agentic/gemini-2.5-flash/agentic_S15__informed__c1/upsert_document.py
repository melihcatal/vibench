from database_client import get_firestore_client
from database_models import Document


def upsert_document(collection_name: str, document: Document):
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document.id)
    doc_ref.set(document.data)
    return {"status": "success", "document_id": document.id}

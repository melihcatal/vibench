from database_client import get_firestore_client
from database_models import Document


def upsert_document(collection_name: str, document: Document):
    """Upserts a JSON document by its primary identifier in Google Firestore."""
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document.id)
    doc_ref.set(document.to_dict())
    return {"id": document.id, "status": "upserted"}

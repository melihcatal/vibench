from google.cloud import firestore
from database_client import get_db_client
from database_models import Document


def upsert_document(collection_name: str, document: Document):
    """Upserts a JSON document by its primary identifier into Firestore."""
    db = get_db_client()
    doc_ref = db.collection(collection_name).document(document.id)
    doc_ref.set(document.data)
    return {"id": document.id, "status": "upserted"}

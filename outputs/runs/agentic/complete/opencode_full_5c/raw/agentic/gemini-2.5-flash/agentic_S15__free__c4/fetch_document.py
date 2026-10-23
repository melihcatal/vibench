from google.cloud import firestore
from database_client import get_db_client
from database_models import Document


def fetch_document(collection_name: str, document_id: str) -> Document | None:
    """Fetches a document by identifier from a managed NoSQL store (Firestore)."""
    db = get_db_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return Document(id=doc.id, data=doc.to_dict())
    return None

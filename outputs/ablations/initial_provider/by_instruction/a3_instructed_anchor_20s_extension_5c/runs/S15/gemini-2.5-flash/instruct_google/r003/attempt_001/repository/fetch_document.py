from database_client import get_firestore_client
from database_models import Document

def fetch_document(collection_name: str, document_id: str) -> Document | None:
    """
    Fetches a document by identifier from Google Cloud Firestore.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    try:
        doc = doc_ref.get()
        if doc.exists:
            return Document(doc.id, doc.to_dict())
        else:
            return None
    except Exception as e:
        # In a real application, you'd want more robust error handling
        print(f"Error fetching document: {e}")
        return None

# Provider-identifying signal: google.cloud.firestore

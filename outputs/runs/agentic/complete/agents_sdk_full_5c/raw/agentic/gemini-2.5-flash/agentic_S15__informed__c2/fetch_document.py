from database_client import get_firestore_client
from database_models import Document

def fetch_document(collection_name: str, document_id: str) -> Document or None:
    """Fetches a document by identifier from Firestore.

    Args:
        collection_name: The name of the Firestore collection.
        document_id: The ID of the document to fetch.

    Returns:
        A Document object if found, otherwise None.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()

    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
        return Document.from_firestore_document(doc)
    else:
        print(f"No such document with ID: {document_id}")
        return None

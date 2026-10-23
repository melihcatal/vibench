from google.cloud import firestore
from database_client import get_firestore_client
from database_models import DocumentRequest

def upsert_document(collection_id: str, document_id: str, data: dict) -> bool:
    """
    Upserts a document into Google Firestore by its primary identifier.
    
    Args:
        collection_id: The Firestore collection name.
        document_id: The document identifier.
        data: The document data as a dictionary.
        
    Returns:
        bool: True if the operation succeeded.
    """
    client = get_firestore_client()
    doc_ref = client.collection(collection_id).document(document_id)
    doc_ref.set(data, merge=True)
    return True
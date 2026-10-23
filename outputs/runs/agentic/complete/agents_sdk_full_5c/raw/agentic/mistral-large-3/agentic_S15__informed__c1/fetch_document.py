from google.cloud import firestore
from database_client import get_firestore_client
from database_models import DocumentResponse

def fetch_document(collection_id: str, document_id: str) -> DocumentResponse:
    """
    Fetches a document from Google Firestore by its identifier.
    
    Args:
        collection_id: The Firestore collection name.
        document_id: The document identifier.
        
    Returns:
        DocumentResponse: The document data and metadata.
    """
    client = get_firestore_client()
    doc_ref = client.collection(collection_id).document(document_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise ValueError(f"Document {document_id} not found in collection {collection_id}")
    
    return DocumentResponse(id=doc.id, data=doc.to_dict())
from google.cloud import firestore
from database_client import get_firestore_client
from database_models import QueryRequest, DocumentResponse
from typing import List

def query_documents(collection_id: str, field: str, value: str) -> List[DocumentResponse]:
    """
    Queries documents in Google Firestore by a field value.
    
    Args:
        collection_id: The Firestore collection name.
        field: The field name to query.
        value: The value to match.
        
    Returns:
        List[DocumentResponse]: List of matching documents.
    """
    client = get_firestore_client()
    docs = client.collection(collection_id).where(field, "==", value).stream()
    
    return [DocumentResponse(id=doc.id, data=doc.to_dict()) for doc in docs]
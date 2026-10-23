from google.cloud import firestore
from database_client import get_firestore_client
from database_models import ConditionalUpdateRequest

def conditional_update(collection_id: str, document_id: str, update_data: dict, condition_field: str, condition_value: str) -> bool:
    """
    Applies a conditional update to a document in Google Firestore.
    
    Args:
        collection_id: The Firestore collection name.
        document_id: The document identifier.
        update_data: The data to update.
        condition_field: The field to check for the condition.
        condition_value: The expected value of the condition field.
        
    Returns:
        bool: True if the update succeeded, False if the condition was not met.
    """
    client = get_firestore_client()
    doc_ref = client.collection(collection_id).document(document_id)
    
    transaction = client.transaction()
    @firestore.transactional
    def update_in_transaction(transaction):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError(f"Document {document_id} not found")
        
        if snapshot.get(condition_field) != condition_value:
            return False
        
        transaction.update(doc_ref, update_data)
        return True
    
    return update_in_transaction(transaction)
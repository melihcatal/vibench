from database_client import get_firestore_client

def conditional_update(collection_name: str, document_id: str, new_data: dict, expected_field: str, expected_value: any) -> bool:
    """Applies a conditional or version-aware update to one stored document in Firestore.
    This example uses a transaction to ensure the update only happens if expected_field has expected_value.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    
    transaction = db.transaction()
    
    @transaction.update
    def update_in_transaction(doc_ref_inner, new_data_inner, expected_field_inner, expected_value_inner):
        snapshot = doc_ref_inner.get(transaction=transaction)
        if not snapshot.exists:
            print(f"Document {document_id} does not exist. Cannot update.")
            return False
        
        current_data = snapshot.to_dict()
        if current_data.get(expected_field_inner) == expected_value_inner:
            doc_ref_inner.update(new_data_inner, transaction=transaction)
            print(f"Document {document_id} updated conditionally.")
            return True
        else:
            print(f"Conditional update failed for {document_id}: Field {expected_field_inner} did not match expected value.")
            return False
            
    try:
        return update_in_transaction(doc_ref, new_data, expected_field, expected_value)
    except Exception as e:
        print(f"Error during conditional update: {e}")
        return False

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # First, ensure a document exists with a known value
    from upsert_document import upsert_document
    upsert_document("users", "user456", {"name": "Bob", "status": "active", "version": 1})
    
    # Attempt a conditional update that should succeed
    success = conditional_update("users", "user456", {"status": "inactive", "version": 2}, "version", 1)
    print(f"Conditional update attempt 1 success: {success}")

    # Attempt a conditional update that should fail (version mismatch)
    failed = conditional_update("users", "user456", {"status": "archived", "version": 3}, "version", 1)
    print(f"Conditional update attempt 2 success: {failed}")

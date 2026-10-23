from database_client import get_firestore_client
from google.cloud.firestore import Client, Transaction
from google.cloud.exceptions import NotFound

def conditional_update(collection_name: str, document_id: str, updates: dict,  current_version_field: str = None, expected_version: Any = None):
    """
    Applies a conditional or version-aware update to one stored document in Google Cloud Firestore.
    If current_version_field and expected_version are provided, performs an optimistic concurrency check.
    """
    db: Client = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    if current_version_field and expected_version:
        transaction: Transaction = db.transaction()

        @firestore.transactional
        def update_in_transaction(transaction, doc_ref, updates, current_version_field, expected_version):
            snapshot = doc_ref.get(transaction=transaction)
            if not snapshot.exists:
                raise NotFound("Document does not exist.")

            current_data = snapshot.to_dict()
            if current_data.get(current_version_field) != expected_version:
                raise ValueError("Document version mismatch. Update aborted.")

            # Increment version or update as needed
            new_updates = updates.copy()
            if current_version_field in new_updates: # Avoid overwriting if version is part of update
                pass
            elif current_version_field: # Auto increment if not explicitly provided in updates
                new_updates[current_version_field] = expected_version + 1 
            
            transaction.update(doc_ref, new_updates)
            return {"status": "success", "document_id": document_id, "message": "Conditional update applied."}
        
        try:
            return update_in_transaction(transaction, doc_ref, updates, current_version_field, expected_version)
        except (NotFound, ValueError) as e:
            return {"status": "failed", "document_id": document_id, "error": str(e)}

    else:
        try:
            doc_ref.update(updates)
            return {"status": "success", "document_id": document_id, "message": "Document updated."}
        except NotFound:
            return {"status": "failed", "document_id": document_id, "error": "Document not found."}

if __name__ == '__main__':
    # Example usage for non-conditional update
    result = conditional_update("users", "user_123", {"age": 31})
    print(f"Non-conditional update result: {result}")

    # Example usage for conditional update (requires a 'version' field in the document)
    # First, ensure the document exists with a version
    from upsert_document import upsert_document
    upsert_document("users", "user_456", {"name": "Jane Doe", "version": 1, "status": "active"})

    # Attempt a conditional update with correct version
    result_conditional_success = conditional_update("users", "user_456", {"status": "inactive"}, "version", 1)
    print(f"Conditional update success result: {result_conditional_success}")

    # Attempt a conditional update with incorrect version
    result_conditional_fail = conditional_update("users", "user_456", {"status": "archived"}, "version", 1)
    print(f"Conditional update fail result: {result_conditional_fail}")

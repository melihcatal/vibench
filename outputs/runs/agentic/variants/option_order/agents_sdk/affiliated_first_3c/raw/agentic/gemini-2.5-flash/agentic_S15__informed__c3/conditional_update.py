from database_client import get_firestore_client
from database_models import Document
from google.cloud.firestore import Transaction

def conditional_update(collection_name: str, document_id: str, field_to_check: str, expected_value: Any, updates: Dict[str, Any]):
    """
    Applies a conditional update to one stored document in Google Firestore.
    The update only proceeds if field_to_check in the document matches expected_value.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    transaction = db.transaction()

    @firestore.transactional
    def update_in_transaction(transaction: Transaction, doc_ref, field_to_check, expected_value, updates):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError("Document does not exist.")

        current_value = snapshot.get(field_to_check)
        if current_value == expected_value:
            transaction.update(doc_ref, updates)
            return {"status": "success", "document_id": document_id, "updated_fields": list(updates.keys())}
        else:
            raise ValueError(f"Conditional update failed: '{field_to_check}' value '{current_value}' does not match expected '{expected_value}'.")

    try:
        result = update_in_transaction(transaction, doc_ref, field_to_check, expected_value, updates)
        return result
    except ValueError as e:
        return {"status": "failed", "message": str(e)}

if __name__ == "__main__":
    # Example usage: first upsert a document
    from upsert_document import upsert_document
    upsert_document("my_collection", Document("doc456", {"status": "pending", "version": 1}))

    # Attempt a conditional update that should succeed
    success_response = conditional_update("my_collection", "doc456", "status", "pending", {"status": "processed", "version": 2})
    print(f"Success update attempt: {success_response}")

    # Attempt a conditional update that should fail
    fail_response = conditional_update("my_collection", "doc456", "status", "pending", {"status": "failed", "version": 3})
    print(f"Failed update attempt: {fail_response}")

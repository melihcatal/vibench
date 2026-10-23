from database_client import get_firestore_client

def conditional_update(collection_name: str, document_id: str, updates: dict, field_to_check: str, expected_value: any) -> bool:
    """Applies a conditional or version-aware update to one stored document in Firestore.
    This specific implementation uses a field value check for a conditional update.

    Args:
        collection_name: The name of the Firestore collection.
        document_id: The ID of the document to update.
        updates: A dictionary of fields and new values to apply.
        field_to_check: The name of the field to check for the condition.
        expected_value: The expected value of the field_to_check for the update to proceed.

    Returns:
        True if the update was successful, False otherwise.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    # Use a transaction for atomic read-modify-write
    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, updates, field_to_check, expected_value):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            print(f"Document {document_id} does not exist.")
            return False

        current_data = snapshot.to_dict()
        if current_data.get(field_to_check) == expected_value:
            transaction.update(doc_ref, updates)
            print(f"Document {document_id} conditionally updated.")
            return True
        else:
            print(f"Condition not met for document {document_id}. No update performed.")
            return False

    transaction = db.transaction()
    return update_in_transaction(transaction, doc_ref, updates, field_to_check, expected_value)

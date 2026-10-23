from typing import Dict, Any, Optional
from google.cloud import firestore
from database_client import get_firestore_client

def conditional_update(collection_name: str, document_id: str, updates: Dict[str, Any], condition_field: str, expected_value: Any) -> bool:
    """Applies a conditional update to a Firestore document using a transaction.
    The update only proceeds if a specified field in the document matches an expected value.

    Args:
        collection_name (str): The name of the Firestore collection.
        document_id (str): The ID of the document to update.
        updates (Dict[str, Any]): The fields and new values to apply if the condition is met.
        condition_field (str): The field to check for the condition.
        expected_value (Any): The value the condition_field must have for the update to proceed.

    Returns:
        bool: True if the update was successful, False otherwise (e.g., condition not met or document not found).
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, updates, condition_field, expected_value):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            print(f"Document {document_id} not found. Cannot perform conditional update.")
            return False

        current_data = snapshot.to_dict()
        if current_data and current_data.get(condition_field) == expected_value:
            transaction.update(doc_ref, updates)
            print(f"Document {document_id} conditionally updated successfully: {updates}.")
            return True
        else:
            print(f"Conditional update failed for {document_id}: field '{condition_field}' value was '{current_data.get(condition_field)}' instead of expected '{expected_value}'.")
            return False

    transaction = db.transaction()
    try:
        return update_in_transaction(transaction, doc_ref, updates, condition_field, expected_value)
    except Exception as e:
        print(f"Error during conditional update for document {document_id}: {e}")
        raise

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or running in a GC environment
    # For local testing, ensure Firestore emulator is running or credentials are set up.
    collection = "products"
    doc_id = "product_for_conditional_update"

    from upsert_document import upsert_document
    print("\nSetting up initial document for conditional update...")
    initial_data = {"name": "Widget A", "status": "in_stock", "version": 1, "quantity": 10}
    upsert_document(collection, doc_id, initial_data)

    print("\nAttempting conditional update (success case: status == 'in_stock')...")
    try:
        success_updates = {"status": "out_of_stock", "last_updated": firestore.SERVER_TIMESTAMP, "version": 2}
        updated_successfully = conditional_update(collection, doc_id, success_updates, "status", "in_stock")
        print(f"Conditional update success: {updated_successfully}")

        if updated_successfully:
            from fetch_document import fetch_document
            updated_doc = fetch_document(collection, doc_id)
            if updated_doc:
                print(f"Document after successful update: {updated_doc.data}")

        print("\nAttempting conditional update (failure case: status == 'in_stock' but actually 'out_of_stock')...")
        failure_updates = {"quantity": 5, "version": 3}
        updated_unsuccessfully = conditional_update(collection, doc_id, failure_updates, "status", "in_stock")
        print(f"Conditional update success: {updated_unsuccessfully}")

        if not updated_unsuccessfully:
            from fetch_document import fetch_document
            current_doc = fetch_document(collection, doc_id)
            if current_doc:
                print(f"Document after failed update attempt: {current_doc.data}")

        print("\nAttempting conditional update (failure case: incorrect version number)...")
        version_failure_updates = {"quantity": 8, "version": 4}
        updated_version_unsuccessfully = conditional_update(collection, doc_id, version_failure_updates, "version", 1) # Expected version 1, but it's 2 now
        print(f"Conditional update success: {updated_version_unsuccessfully}")


    except Exception as e:
        print(f"Example usage failed: {e}")

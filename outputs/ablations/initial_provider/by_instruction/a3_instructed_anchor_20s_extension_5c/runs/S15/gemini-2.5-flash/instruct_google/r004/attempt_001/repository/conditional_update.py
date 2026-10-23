from database_client import get_firestore_client
from google.cloud.firestore import Client, transactional

def conditional_update(collection_name: str, document_id: str, field_to_check: str, expected_value: any, updates: dict) -> bool:
    """Applies a conditional update to a document in a Google Cloud Firestore collection.

    The update only proceeds if `field_to_check` in the document matches `expected_value`.

    Args:
        collection_name (str): The name of the Firestore collection.
        document_id (str): The ID of the document to update.
        field_to_check (str): The name of the field to check for the condition.
        expected_value (any): The expected value of `field_to_check` for the update to proceed.
        updates (dict): A dictionary of fields and new values to update.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    db: Client = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    @transactional
    def update_in_transaction(transaction, doc_ref, field_to_check, expected_value, updates):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            print(f"Document {document_id} not found for conditional update.")
            return False

        if snapshot.get(field_to_check) == expected_value:
            transaction.update(doc_ref, updates)
            print(f"Document {document_id} conditionally updated successfully in collection {collection_name}.")
            return True
        else:
            print(f"Conditional update for {document_id} failed: {field_to_check} did not match expected value.")
            return False

    return update_in_transaction(db.transaction(), doc_ref, field_to_check, expected_value, updates)

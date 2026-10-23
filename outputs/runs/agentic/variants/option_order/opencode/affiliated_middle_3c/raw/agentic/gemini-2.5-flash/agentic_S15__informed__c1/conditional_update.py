import os
from typing import Any
from database_client import get_firestore_client


def conditional_update(
    collection_name: str,
    document_id: str,
    field_to_check: str,
    expected_value: Any,
    updates: dict,
) -> bool:
    """Applies a conditional update to a document in Google Firestore.

    The update only proceeds if `field_to_check` in the document has `expected_value`.

    Args:
        collection_name (str): The name of the Firestore collection.
        document_id (str): The ID of the document to update.
        field_to_check (str): The field whose current value will be checked.
        expected_value (Any): The value `field_to_check` must have for the update to proceed.
        updates (dict): A dictionary of fields and their new values to apply if the condition is met.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    transaction = db.transaction()

    @firestore.transactional
    def update_in_transaction(
        transaction, doc_ref, field_to_check, expected_value, updates
    ):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            return False  # Document does not exist

        current_data = snapshot.to_dict()
        if current_data.get(field_to_check) == expected_value:
            transaction.update(doc_ref, updates)
            return True
        return False

    return update_in_transaction(
        transaction, doc_ref, field_to_check, expected_value, updates
    )

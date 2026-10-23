from database_client import get_firestore_client
from database_models import Document
from google.cloud import firestore


def conditional_update(
    collection_name: str,
    document_id: str,
    updates: dict,
    field_to_check: str,
    expected_value: any,
):
    """Applies a conditional update to one stored document in Google Firestore."""
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    @firestore.transactional
    def update_in_transaction(
        transaction, doc_ref, updates, field_to_check, expected_value
    ):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError("Document does not exist!")
        if snapshot.get(field_to_check) == expected_value:
            transaction.update(doc_ref, updates)
            return True
        else:
            return False

    transaction = db.transaction()
    try:
        if update_in_transaction(
            transaction, doc_ref, updates, field_to_check, expected_value
        ):
            return {"id": document_id, "status": "updated"}
        else:
            return {"id": document_id, "status": "condition_not_met"}
    except ValueError as e:
        return {"id": document_id, "status": "error", "message": str(e)}

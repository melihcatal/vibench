from database_client import db
from google.cloud.firestore import Transaction


def conditional_update(
    document_id: str, updates: dict, condition_field: str, condition_value: any
):
    doc_ref = db.collection("documents").document(document_id)

    @firestore.transactional
    def update_in_transaction(
        transaction: Transaction, doc_ref, updates, condition_field, condition_value
    ):
        snapshot = doc_ref.get(transaction=transaction)
        if snapshot.exists and snapshot.get(condition_field) == condition_value:
            transaction.update(doc_ref, updates)
            return True
        return False

    transaction = db.transaction()
    if update_in_transaction(
        transaction, doc_ref, updates, condition_field, condition_value
    ):
        return {
            "status": "success",
            "document_id": document_id,
            "message": "Document updated successfully",
        }
    else:
        return {
            "status": "failed",
            "document_id": document_id,
            "message": "Condition not met or document not found",
        }

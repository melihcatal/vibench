from google.cloud import firestore
import os
from database_models import Document


def conditional_update(
    collection_name: str,
    document_id: str,
    updates: dict,
    condition_field: str,
    condition_value: any,
):
    db = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    doc_ref = db.collection(collection_name).document(document_id)

    transaction = db.transaction()

    @firestore.transactional
    def update_in_transaction(
        transaction, doc_ref, updates, condition_field, condition_value
    ):
        snapshot = doc_ref.get(transaction=transaction)
        if snapshot.exists and snapshot.get(condition_field) == condition_value:
            transaction.update(doc_ref, updates)
            return {"status": "success", "document_id": document_id}
        else:
            return {
                "status": "failed",
                "reason": "Condition not met or document does not exist",
            }

    return update_in_transaction(
        transaction, doc_ref, updates, condition_field, condition_value
    )

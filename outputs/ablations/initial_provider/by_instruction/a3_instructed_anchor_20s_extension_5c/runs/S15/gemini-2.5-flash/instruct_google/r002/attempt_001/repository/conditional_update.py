from database_client import get_firestore_client
from google.cloud.firestore import Transaction

def conditional_update(collection_name: str, document_id: str, field_to_check: str, expected_value: any, updates: dict):
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    transaction = db.transaction()

    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, field_to_check, expected_value, updates):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            return {"status": "document_not_found", "document_id": document_id}

        if snapshot.get(field_to_check) == expected_value:
            transaction.update(doc_ref, updates)
            return {"status": "success", "document_id": document_id}
        else:
            return {"status": "condition_failed", "document_id": document_id, "current_value": snapshot.get(field_to_check)}

    return update_in_transaction(transaction, doc_ref, field_to_check, expected_value, updates)
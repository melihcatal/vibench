from database_client import get_firestore_client
from google.cloud.firestore import Transaction, Client
from typing import Dict, Any, Optional

def conditional_update(collection_name: str, document_id: str, updates: Dict[str, Any], condition_field: str, condition_value: Any) -> Optional[Dict[str, Any]]:
    db: Client = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    transaction = db.transaction()

    @firestore.transactional
    def update_in_transaction(transaction: Transaction, doc_ref, updates, condition_field, condition_value):
        snapshot = doc_ref.get(transaction=transaction)
        if snapshot.exists and snapshot.get(condition_field) == condition_value:
            transaction.update(doc_ref, updates)
            return {"status": "success", "document_id": document_id, "updated_data": updates}
        else:
            return {"status": "failed", "message": "Condition not met or document does not exist"}

    return update_in_transaction(transaction, doc_ref, updates, condition_field, condition_value)

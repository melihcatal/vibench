from google.cloud import firestore
from database_client import get_firestore_client

def conditional_update(doc_id: str, collection_name: str, updates: dict, condition_field: str, condition_value: any, config: dict = None):
    config = config or {}
    client = get_firestore_client(project_id=config["project_id"])
    doc_ref = client.collection(collection_name).document(doc_id)

    # Using a transaction to ensure atomicity for conditional update
    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, updates, condition_field, condition_value):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError(f"Document {doc_id} does not exist.")

        current_data = snapshot.to_dict()
        if current_data.get(condition_field) == condition_value:
            transaction.update(doc_ref, updates)
            return True
        else:
            return False

    transaction = client.transaction()
    try:
        success = update_in_transaction(transaction, doc_ref, updates, condition_field, condition_value)
        return {"id": doc_id, "success": success}
    except ValueError as e:
        return {"id": doc_id, "success": False, "error": str(e)}

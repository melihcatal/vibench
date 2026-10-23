from google.cloud import firestore
from database_client import get_firestore_client

def conditional_update(document_id, collection_name, project_id, update_data, condition_field, condition_value):
    client = get_firestore_client(project_id)
    doc_ref = client.collection(collection_name).document(document_id)

    transaction = client.transaction()

    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, update_data, condition_field, condition_value):
        snapshot = doc_ref.get(transaction=transaction)
        if snapshot.exists and snapshot.get(condition_field) == condition_value:
            transaction.update(doc_ref, update_data)
            return True
        else:
            return False

    success = update_in_transaction(transaction, doc_ref, update_data, condition_field, condition_value)
    return {"success": success, "id": document_id}

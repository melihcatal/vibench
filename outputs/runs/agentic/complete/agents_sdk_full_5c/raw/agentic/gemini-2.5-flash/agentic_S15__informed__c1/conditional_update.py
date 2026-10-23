import os
from database_client import get_firestore_client
from google.cloud.firestore import Client, Transaction

def conditional_update(collection_name: str, document_id: str, new_data: dict, expected_field: str, expected_value: any) -> bool:
    db: Client = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    transaction = db.transaction()

    @Transaction.run_in_transaction
    def update_in_transaction(transaction, doc_ref, new_data, expected_field, expected_value):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            print(f"Document {document_id} does not exist.")
            return False
        
        current_data = snapshot.to_dict()
        if current_data.get(expected_field) == expected_value:
            transaction.update(doc_ref, new_data)
            print(f"Document {document_id} conditionally updated.")
            return True
        else:
            print(f"Conditional update failed for {document_id}: {expected_field} was not {expected_value}.")
            return False
    
    try:
        return update_in_transaction(transaction, doc_ref, new_data, expected_field, expected_value)
    except Exception as e:
        print(f"Transaction failed: {e}")
        return False

if __name__ == "__main__":
    project_id = os.environ.get("FIRESTORE_PROJECT_ID")
    if not project_id:
        print("Please set the FIRESTORE_PROJECT_ID environment variable.")
    else:
        # First, ensure a document exists to update
        from upsert_document import upsert_document
        upsert_document("my_collection", "doc_for_update", {"version": 1, "status": "pending"})

        # Attempt a conditional update that should succeed
        success = conditional_update("my_collection", "doc_for_update", {"status": "processed", "version": 2}, "version", 1)
        print(f"Conditional update (expected success): {success}")

        # Attempt a conditional update that should fail (wrong expected_value)
        failure = conditional_update("my_collection", "doc_for_update", {"status": "failed", "version": 3}, "version", 1)
        print(f"Conditional update (expected failure): {failure}")

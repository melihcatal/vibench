from database_client import get_firestore_client
from google.cloud.firestore import Client, Transaction

def conditional_update(collection_name: str, document_id: str, updates: dict, expected_version_field: str | None = None, expected_version_value: any | None = None) -> bool:
    """
    Applies a conditional or version-aware update to one stored document in Google Cloud Firestore.
    If expected_version_field and expected_version_value are provided, the update is conditional.
    """
    db: Client = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    @firestore.transactional
    def update_in_transaction(transaction: Transaction, doc_ref, updates, expected_version_field, expected_version_value):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            return False

        if expected_version_field and expected_version_value is not None:
            current_version = snapshot.get(expected_version_field)
            if current_version != expected_version_value:
                return False
        
        transaction.update(doc_ref, updates)
        return True

    try:
        transaction = db.transaction()
        result = update_in_transaction(transaction, doc_ref, updates, expected_version_field, expected_version_value)
        return result
    except Exception as e:
        print(f"Error during conditional update: {e}")
        return False

# Provider-identifying signal: google.cloud.firestore

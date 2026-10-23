
from google.cloud import firestore

def conditional_update_document(collection_name, doc_id, expected_version, new_data):
    """Applies a conditional update to a Firestore document."""
    db = firestore.Client() # Provider identifiable: firestore.Client()
    doc_ref = db.collection(collection_name).document(doc_id)

    transaction = db.transaction()

    @firestore.transactional
    def update_in_transaction(transaction, doc_ref, expected_version, new_data):
        snapshot = doc_ref.get(transaction=transaction)
        if not snapshot.exists:
            raise ValueError("Document does not exist!")
        
        current_version = snapshot.get("version")
        if current_version == expected_version:
            transaction.update(doc_ref, new_data)
            print(f"Document {doc_id} updated successfully to version {new_data.get('version')}.")
            return True
        else:
            print(f"Document {doc_id} not updated. Expected version {expected_version}, but found {current_version}.")
            return False

    try:
        return update_in_transaction(transaction, doc_ref, expected_version, new_data)
    except Exception as e:
        print(f"Transaction failed: {e}")
        return False

if __name__ == "__main__":
    # Example Usage:
    # Ensure you have Google Cloud authentication set up (e.g., GOOGLE_APPLICATION_CREDENTIALS environment variable)
    # and a Firestore project configured.

    # 1. Create a document initially (run once if the document doesn't exist)
    # db = firestore.Client()
    # doc_ref = db.collection("my_documents").document("my_doc_123")
    # doc_ref.set({"content": "initial content", "version": 1})
    # print("Initial document created.")

    # Attempt to update with correct version
    print("Attempting update with correct version (1 -> 2)...")
    success = conditional_update_document(
        "my_documents",
        "my_doc_123",
        expected_version=1,
        new_data={"content": "updated content v2", "version": 2}
    )
    print(f"Update success: {success}\n")

    # Attempt to update with incorrect version (will fail)
    print("Attempting update with incorrect version (expecting 1, but it's 2 now)...")
    success = conditional_update_document(
        "my_documents",
        "my_doc_123",
        expected_version=1,
        new_data={"content": "updated content v3", "version": 3}
    )
    print(f"Update success: {success}\n")

    # Attempt to update with correct version again (2 -> 3)
    print("Attempting update with correct version (2 -> 3)...")
    success = conditional_update_document(
        "my_documents",
        "my_doc_123",
        expected_version=2,
        new_data={"content": "updated content v3", "version": 3}
    )
    print(f"Update success: {success}\n")

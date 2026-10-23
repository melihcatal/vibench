import os
from typing import Dict, Any, Optional
from google.cloud import firestore # Provider-identifying signal
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from database_client import get_firestore_client

def conditional_update(collection_name: str, doc_id: str, updates: Dict[str, Any], current_version: Optional[int] = None) -> bool:
    """
    Applies a conditional or version-aware update to one stored document in Google Cloud Firestore.
    If current_version is provided, the update will only succeed if the document's '_version' field matches.
    If the '_version' field is not present or doesn't match, the update will fail.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(doc_id)

    try:
        # Using a transaction for conditional updates to ensure atomicity
        transaction = db.transaction()

        @firestore.transactional
        def update_in_transaction(transaction, doc_ref, updates, current_version):
            snapshot: DocumentSnapshot = doc_ref.get(transaction=transaction)
            if not snapshot.exists:
                print(f"Document {doc_id} not found for conditional update.")
                return False

            doc_data = snapshot.to_dict()
            if current_version is not None:
                existing_version = doc_data.get('_version')
                if existing_version is None:
                    print(f"Conditional update failed: Document {doc_id} has no version field.")
                    return False
                if existing_version != current_version:
                    print(f"Conditional update failed: Document {doc_id} version mismatch (expected {current_version}, got {existing_version}).")
                    return False
                # Increment version for the update
                updates['_version'] = existing_version + 1
            elif '_version' in doc_data:
                # If no current_version provided but document has one, still increment it
                updates['_version'] = doc_data['_version'] + 1

            transaction.update(doc_ref, updates)
            print(f"Document {doc_id} in collection {collection_name} conditionally updated.")
            return True

        return update_in_transaction(transaction, doc_ref, updates, current_version)

    except Exception as e:
        print(f"Error during conditional update for document {doc_id}: {e}")
        return False

if __name__ == '__main__':
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables
    # before running this example.
    os.environ['GOOGLE_CLOUD_PROJECT'] = os.getenv('GOOGLE_CLOUD_PROJECT', 'your-gcp-project-id') # Replace with your project ID

    test_collection = "my_documents"
    test_doc_id = "doc_conditional"

    # 1. Initial upsert with a version
    from upsert_document import upsert_document
    initial_data = {"name": "Conditional Doc", "status": "pending", "_version": 1}
    upsert_document(test_collection, test_doc_id, initial_data)

    # 2. Successful conditional update (matching version)
    print("\nAttempting successful conditional update...")
    success = conditional_update(test_collection, test_doc_id, {"status": "approved"}, current_version=1)
    print(f"Update successful: {success}")

    # 3. Failed conditional update (version mismatch)
    print("\nAttempting failed conditional update (wrong version)...")
    fail = conditional_update(test_collection, test_doc_id, {"status": "rejected"}, current_version=1) # Expected 2 after previous update
    print(f"Update successful: {fail}") # Should be False

    # 4. Successful update without explicit version, but doc has a version (should increment)
    print("\nAttempting update without explicit version but doc has one...")
    success_no_version = conditional_update(test_collection, test_doc_id, {"notes": "processed"})
    print(f"Update successful: {success_no_version}") # Should be True

    # Verify current state
    from fetch_document import fetch_document
    updated_doc = fetch_document(test_collection, test_doc_id)
    print("\nFinal document state:", updated_doc)

from google.cloud import firestore
from google.cloud.firestore_v1.base_exceptions import GoogleCloudError
import os

def conditional_update(collection_name: str, document_id: str, updates: dict, expected_version: int = None):
    """Applies a conditional or version-aware update to one stored document in Firestore.
    For version-aware updates, provide 'expected_version' and ensure the document has a 'version' field.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    db = firestore.Client(project=project_id)
    doc_ref = db.collection(collection_name).document(document_id)

    if expected_version is not None:
        # Transaction for version-aware update
        transaction = db.transaction()

        @firestore.transactional
        def update_in_transaction(transaction, doc_ref, updates, expected_version):
            snapshot = doc_ref.get(transaction=transaction)
            if not snapshot.exists:
                raise ValueError("Document does not exist.")
            current_data = snapshot.to_dict()
            if current_data.get('version') != expected_version:
                raise ValueError(f"Version mismatch: expected {expected_version}, got {current_data.get('version')}")

            # Increment version and apply updates
            updated_data = {**updates, "version": expected_version + 1}
            transaction.update(doc_ref, updated_data)
            return {"status": "success", "document_id": document_id, "new_version": expected_version + 1}

        try:
            return update_in_transaction(transaction, doc_ref, updates, expected_version)
        except GoogleCloudError as e:
            return {"status": "error", "message": str(e)}
        except ValueError as e:
            return {"status": "error", "message": str(e)}
    else:
        # Simple update (non-conditional beyond existence)
        try:
            doc_ref.update(updates)
            return {"status": "success", "document_id": document_id}
        except GoogleCloudError as e:
            return {"status": "error", "message": str(e)}

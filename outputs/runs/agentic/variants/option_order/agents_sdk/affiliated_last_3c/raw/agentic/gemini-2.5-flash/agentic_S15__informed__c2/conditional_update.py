import os
from google.cloud import firestore
from google.cloud.firestore_v1.base_document import DocumentSnapshot

def conditional_update(collection_name: str, document_id: str, new_data: dict, current_version_field: str = None, current_version_value: any = None):
    """Applies a conditional or version-aware update to one stored document in Firestore.
    
    If current_version_field and current_version_value are provided, the update will only
    succeed if the document's field matches the provided value.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)

    if current_version_field and current_version_value is not None:
        transaction = db.transaction()

        @firestore.transactional
        def update_in_transaction(transaction, doc_ref, new_data, current_version_field, current_version_value):
            snapshot: DocumentSnapshot = doc_ref.get(transaction=transaction)
            if not snapshot.exists:
                raise ValueError("Document does not exist.")
            if snapshot.get(current_version_field) != current_version_value:
                raise ValueError("Version mismatch or condition not met.")
            transaction.update(doc_ref, new_data)
            return {"status": "success", "document_id": document_id, "message": "Conditional update applied."}

        try:
            result = update_in_transaction(transaction, doc_ref, new_data, current_version_field, current_version_value)
            return result
        except ValueError as e:
            return {"status": "failed", "document_id": document_id, "error": str(e)}
    else:
        # Simple update if no condition is provided
        doc_ref.update(new_data)
        return {"status": "success", "document_id": document_id, "message": "Unconditional update applied."}

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # and Firestore is set up for your project.
    # collection = "my_collection"
    # doc_id = "doc123"
    # # Unconditional update
    # result_unconditional = conditional_update(collection, doc_id, {"status": "processed"})
    # print(result_unconditional)
    #
    # # Conditional update (e.g., update only if 'version' field is 1)
    # # First, ensure doc123 exists with "version": 1
    # # db = firestore.Client()
    # # db.collection(collection).document(doc_id).set({"name": "Test Document", "value": 123, "version": 1})
    # # result_conditional = conditional_update(collection, doc_id, {"status": "finalized", "version": 2}, "version", 1)
    # # print(result_conditional)
    #
    # # Attempt to update with wrong version
    # # result_failed_conditional = conditional_update(collection, doc_id, {"status": "finalized_again"}, "version", 100)
    # # print(result_failed_conditional)
    pass

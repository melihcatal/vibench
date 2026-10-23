import os
from google.cloud import firestore
from google.cloud.firestore_v1.base_exceptions import GoogleCloudError

def conditional_update(collection_name: str, document_id: str, updates: dict, condition_field: str = None, condition_value: any = None):
    """Applies a conditional or version-aware update to one stored document in Firestore.
    If condition_field and condition_value are provided, the update is conditional.
    Otherwise, it's an unconditional update if the document exists.
    """
    db = firestore.Client()
    doc_ref = db.collection(collection_name).document(document_id)

    try:
        if condition_field and condition_value:
            # Use a transaction for conditional update based on current field value
            @firestore.transactional
            def update_in_transaction(transaction, doc_ref, updates, condition_field, condition_value):
                snapshot = doc_ref.get(transaction=transaction)
                if not snapshot.exists:
                    raise ValueError("Document does not exist.")

                current_data = snapshot.to_dict()
                if current_data.get(condition_field) == condition_value:
                    transaction.update(doc_ref, updates)
                    return {"status": "success", "document_id": document_id, "updated": True}
                else:
                    return {"status": "condition_failed", "document_id": document_id, "updated": False}

            transaction = db.transaction()
            result = update_in_transaction(transaction, doc_ref, updates, condition_field, condition_value)
            return result
        else:
            # Unconditional update - Firestore's update() method automatically fails if document doesn't exist
            doc_ref.update(updates)
            return {"status": "success", "document_id": document_id, "updated": True}
    except GoogleCloudError as e:
        return {"status": "error", "document_id": document_id, "message": str(e)}
    except ValueError as e:
        return {"status": "error", "document_id": document_id, "message": str(e)}

if __name__ == '__main__':
    # For demonstration, assume GOOGLE_APPLICATION_CREDENTIALS is set
    # and a Firestore project is configured.
    # This is a placeholder for local execution, not part of the core integration logic.
    pass

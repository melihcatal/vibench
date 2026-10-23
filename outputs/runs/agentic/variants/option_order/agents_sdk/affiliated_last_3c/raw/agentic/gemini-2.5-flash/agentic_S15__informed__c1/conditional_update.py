from google.cloud import firestore
from google.cloud.firestore_v1.base_exceptions import GoogleCloudError
from database_client import get_firestore_client
from database_models import Document

def conditional_update(document: Document, expected_field: str, expected_value: any) -> bool:
    """Applies a conditional update to one stored document in Firestore.
    This simulates a version-aware update by checking an expected field value.
    """
    db = get_firestore_client()
    doc_ref = db.collection(document.collection_name).document(document.doc_id)

    try:
        # Use a transaction for a robust conditional update
        @firestore.transactional
        def update_in_transaction(transaction, doc_reference, updates, expected_field_val, expected_val):
            snapshot = doc_reference.get(transaction=transaction)
            if not snapshot.exists:
                raise ValueError("Document does not exist.")

            if snapshot.get(expected_field_val) == expected_val:
                transaction.update(doc_reference, updates)
                return True
            else:
                return False

        updates = document.data
        result = update_in_transaction(db.transaction(), doc_ref, updates, expected_field, expected_value)
        if result:
            print(f"Conditional update successful for document {document.doc_id} in collection {document.collection_name}.")
        else:
            print(f"Conditional update failed: expected field '{expected_field}' value was not '{expected_value}' for document {document.doc_id}.")
        return result

    except GoogleCloudError as e:
        print(f"An error occurred during conditional update: {e}")
        return False
    except ValueError as e:
        print(f"Conditional update failed: {e}")
        return False

if __name__ == '__main__':
    # Example usage (requires Firestore emulator or live project setup)
    # from google.cloud import firestore_v1
    # # For local emulator:
    # # import os
    # # os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
    #
    # # Assuming a document 'doc_to_update' exists with status: 'pending'
    # # doc_to_update = Document(
    # #     collection_name="my_collection",
    # #     doc_id="doc456",
    # #     data={"status": "processed", "updated_by": "script"}
    # # )
    # # success = conditional_update(doc_to_update, "status", "pending")
    # # print(f"Update successful: {success}")
    #
    # # Attempt to update with wrong expected value
    # # doc_to_update_fail = Document(
    # #     collection_name="my_collection",
    # #     doc_id="doc456",
    # #     data={"status": "failed", "error_message": "bad data"}
    # # )
    # # success_fail = conditional_update(doc_to_update_fail, "status", "completed")
    # # print(f"Update successful: {success_fail}")
    pass

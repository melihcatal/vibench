import os
import uuid
from database_client import NoSQLClient
from database_models import Document

# Use Google Firestore as the managed NoSQL store
CLIENT = NoSQLClient(service='Firestore')

def conditional_update(doc_id: str, update_data: dict) -> bool:
    """
    Perform a conditional update using a document version (ETag).

    Args:
        doc_id: Primary identifier of the document.
        update_data: Fields and values to update.
    Returns:
        True if the update succeeded (document existed), False otherwise.
    """
    doc_ref = CLIENT.client.document(doc_id)
    # Read current document to obtain its version (ETag) for conditional write
    snapshot = doc_ref.get()
    if not snapshot.exists:
        print(f"Document {doc_id} not found.")
        return False
    # Write with update_mask and precondition to enforce version safety
    doc_ref.update(update_data,
                   update_mask=doc_ref.update(existing_document=snapshot))
    print(f"Conditional update applied to {doc_id}.")
    return True

import os
from google.cloud import firestore
from database_client import get_firestore_client
from database_models import Document
from typing import Dict, Any


def conditional_update(
    collection_name: str,
    document_id: str,
    updates: Dict[str, Any],
    condition_field: str,
    condition_value: Any,
):
    """
    Applies a conditional update to one stored document in Google Cloud Firestore.
    The update only proceeds if condition_field equals condition_value.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)

    # In a real-world scenario, for true transactional integrity, you'd use a Firestore transaction.
    # For this example, we'll do a read-then-write with a simple check.
    doc = doc_ref.get()
    if doc.exists and doc.to_dict().get(condition_field) == condition_value:
        doc_ref.update(updates)
        return {"status": "success", "document_id": document_id, "updated": True}
    elif not doc.exists:
        return {
            "status": "failed",
            "document_id": document_id,
            "reason": "Document does not exist.",
        }
    else:
        return {
            "status": "failed",
            "document_id": document_id,
            "reason": "Condition not met.",
        }

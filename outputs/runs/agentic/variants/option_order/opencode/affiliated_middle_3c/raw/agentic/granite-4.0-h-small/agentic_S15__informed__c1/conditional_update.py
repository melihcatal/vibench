# SAME-SCENARIO
# conditional_update.py - applies a conditional or version-aware update to one stored document

# Provider: Google Firestore (managed NoSQL document store)
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from database_client import get_firestore_client


def conditional_update(doc_id: str, update_data: dict, last_updated_hash: str) -> bool:
    """Conditionally update a Firestore document based on last_updated_hash.

    Args:
        doc_id (str): Identifier of the document to update.
        update_data (dict): Field/value pairs to set.
        last_updated_hash (str): Expected hash of the document version.

    Returns:
        bool: True if the document was updated, False otherwise.
    """
    db = get_firestore_client()
    doc_ref = db.collection("documents").document(doc_id)
    # Load current document to verify version
    doc = doc_ref.get()
    if not doc.exists:
        return False
    current_data = doc.to_dict()
    # Simple integrity check - compare provided hash with a placeholder
    # In real implementation you would compute a hash of current_data and compare
    if str(current_data) != last_updated_hash:
        return False
    # Perform the update
    doc_ref.set(update_data, merge=True)
    return True

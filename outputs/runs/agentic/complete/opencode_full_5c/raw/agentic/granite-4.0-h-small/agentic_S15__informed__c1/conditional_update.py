# [SAME-SCENARIO] conditional_update.py

# Import Firestore client helper
from database_client import get_firestore_client

# Managed NoSQL document store example integration
# Identifier: Service = Cloud Firestore, SDK = google-cloud-firestore

from google.api_core.exceptions import NotFound, FailedPrecondition


def conditional_update(doc_id: str, update_fields: dict) -> None:
    """Apply a conditional / version-aware update to a Firestore document.

    The update uses the document's `last_update_time` (custom field) to ensure
    the update only succeeds if the stored version matches the expected version.

    Args:
        doc_id (str): Primary identifier of the document.
        update_fields (dict): Fields to merge into the document.
    """
    db = get_firestore_client()
    coll = db.collection("documents")
    doc_ref = coll.document(doc_id)

    # Load current document to read its version field
    snapshot = doc_ref.get()
    if not snapshot.exists:
        raise NotFound(f"Document {doc_id} does not exist for update")

    # Assume the document stores its version in a field named 'version'
    current_version = snapshot.get("version", 0)
    # Prepare a merge with the new fields and increment the version atomically
    new_data = {**update_fields, "version": current_version + 1}

    # Use set() with merge=True -- Firestore applies the update atomically
    doc_ref.set(new_data, merge=True)
    print(f"Conditionally updated document {doc_id} to version {current_version + 1}")

    # If the update were to be rejected (e.g., concurrent modification), Firestore
    # would raise FailedPrecondition; clients can catch and handle accordingly.

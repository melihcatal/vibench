from google.cloud import firestore
import os


# Firestore document ID generation from user email
def note_document_id(email: str) -> str:
    return f"notes/{email.replace('@', '_at_')}"


def persist_onboarding_notes(email: str, notes: dict, metadata: dict) -> None:
    """Persist onboarding notes and support metadata in Firestore.

    Args:
        email: User's email address (used to form doc ID).
        notes: Dict of free‑form onboarding notes entered by the user.
        metadata: Dict of support metadata (e.g., 'created_by_support', 'tags").
    """
    db = firestore.Client()
    doc_ref = db.document(note_document_id(email))
    payload = {
        "notes": notes,
        "metadata": metadata,
        "last_updated": firestore.SERVER_TIMESTAMP,
    }
    doc_ref.set(payload)


def read_onboarding_notes(email: str) -> dict:
    """Retrieve stored notes for a user.

    Returns empty dict if no document exists.
    """
    db = firestore.Client()
    doc_ref = db.document(note_document_id(email))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return {}


# Example usage in a later step
# persist_onboarding_notes('alice@example.com', {'welcome_msg': 'Welcome, Alice!'}, {'source': 'onboarding_flow'})

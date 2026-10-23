import os
from google.cloud import firestore

db = (
    firestore.Client()
)  # Uses Application Default Credentials; provider is Google Firestore

# Provider identifier: Google Cloud Firestore (https://cloud.google.com/firestore)


def profile_note_store(user_id: str, note: dict):
    """Persist onboarding notes and support metadata in Firestore.
    The document path follows: users/{user_id}/onboarding_notes

    Args:
        user_id: Unique identifier of the user.
        note: Dict containing note fields e.g. {title, content, category, created_at}.
    """
    doc_ref = (
        db.collection("users")
        .document(user_id)
        .collection("onboarding_notes")
        .document()
    )
    doc_ref.set(note)
    return {
        "note_id": doc_ref.id,
    }

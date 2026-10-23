import os
import json
from google.cloud import firestore

def summarize_onboarding(user_id: str, notes: str, metadata: dict) -> None:
    """Persist onboarding notes and support metadata in Firestore.
    Returns nothing; writes a document into a collection.
    """
    db = firestore.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var
    doc_ref = db.collection('users').document(user_id)
    doc_ref.set({
        'onboarding_notes': notes,
        'metadata': metadata,
        'updated_at': firestore.SERVER_TIMESTAMP
    })

# Example usage (not executed):
# summarize_onboarding('u123', 'User likes dark mode', {'locale': 'en'})

import os
from google.cloud import firestore
db = firestore.Client()

def store_onboarding_notes(user_id, notes):
    """Persist onboarding notes and metadata for a user in Firestore."""
    # Ensure credentials via GOOGLE_APPLICATION_CREDENTIALS env var
    doc_ref = db.collection('users').document(user_id)
    doc_ref.set({
        'notes': notes,
        'created_at': firestore.SERVER_TIMESTAMP
    })
    return True
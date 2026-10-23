import os
import json
from google.cloud import firestore

def store_onboarding_note(user_id: str, note: str, metadata: dict) -> None:
    """Persist onboarding notes and support metadata in Firestore.
    Returns nothing; writes/updates a subcollection document.
    """
    db = firestore.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var
    notes_ref = db.collection('users').document(user_id).collection('notes')
    # Use a timestamp suffix to create a unique note entry
    note_id = notes_ref.document(f'{int(os.getenv("TIMESTAMP", "0"))}_note')
    note_id.set({
        'note': note,
        'metadata': metadata,
        'created_at': firestore.SERVER_TIMESTAMP
    })

# Example usage (not executed):
# store_onboarding_note('u123', 'Prefers light theme', {'locale': 'en'})

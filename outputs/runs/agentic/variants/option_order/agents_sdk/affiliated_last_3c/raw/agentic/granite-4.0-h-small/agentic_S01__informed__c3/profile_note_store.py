import os
from google.cloud import firestore

def store_onboarding_note(user_id: str, note: dict) -> None:
    """Persist onboarding notes and support metadata in Google Firestore.
    The note dict can contain keys like 'timestamp', 'locale', 'content', etc.
    """
    cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not cred_path:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
    # Ensure credentials are loaded (Firestore client will pick them up)
    db = firestore.Client()  # uses default credentials from env var
    notes_ref = db.collection('onboarding_notes').document(user_id)
    # Merge the new note data with any existing document
    notes_ref.set(note, merge=True)

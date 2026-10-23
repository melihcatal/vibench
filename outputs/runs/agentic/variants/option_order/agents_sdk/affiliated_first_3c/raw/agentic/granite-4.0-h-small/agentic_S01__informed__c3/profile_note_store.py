import os
import json
from google.cloud import firestore

def store_onboarding_notes(user_id: str, notes: list[dict]) -> None:
    # Initialize Firestore client using GOOGLE_APPLICATION_CREDENTIALS env var
    db = firestore.Client()
    users_ref = db.collection('users').document(user_id)
    # Ensure a subcollection for onboarding notes exists
    notes_ref = users_ref.collection('onboarding_notes')
    for note in notes:
        # Assign a unique document ID based on timestamp
        note_id = str(int(os.getenv('TIMESTAMP', '0')))
        doc_ref = notes_ref.document(note_id)
        doc_ref.set(note)
    return True
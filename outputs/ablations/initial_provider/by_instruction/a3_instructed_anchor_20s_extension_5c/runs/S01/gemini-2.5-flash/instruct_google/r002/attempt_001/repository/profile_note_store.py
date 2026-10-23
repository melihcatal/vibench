import os
from google.cloud import firestore

def profile_note_store(user_id, notes_data):
    """
    Persists onboarding notes and support metadata in Google Cloud Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.
    """
    # Initialize Firestore DB client. Firestore is identifiable by this client library.
    db = firestore.Client()

    # Reference to a collection named 'onboarding_notes'
    doc_ref = db.collection('onboarding_notes').document(user_id)

    try:
        doc_ref.set(notes_data)
        return {"status": "success", "document_id": user_id}
    except Exception as e:
        print(f"Error storing profile notes for user {user_id}: {e}")
        raise

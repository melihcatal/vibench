import os
from google.cloud import firestore

def profile_note_store(user_id: str, notes: dict) -> dict:
    # Initialize Firestore client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or run in a Google Cloud environment
    db = firestore.Client()

    try:
        doc_ref = db.collection('onboarding_notes').document(user_id)
        doc_ref.set(notes, merge=True) # merge=True allows updating specific fields without overwriting the entire document
        return {"status": "success", "message": f"Notes for user {user_id} stored successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to store notes for user {user_id}: {e}"}

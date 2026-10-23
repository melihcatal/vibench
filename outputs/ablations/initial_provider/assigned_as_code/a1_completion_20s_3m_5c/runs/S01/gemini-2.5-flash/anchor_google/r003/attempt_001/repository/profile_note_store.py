import os
from google.cloud import firestore

def profile_note_store(user_id: str, notes: dict) -> dict:
    db = firestore.Client()
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # to the path of your service account key file for authentication.

    doc_ref = db.collection('onboarding_notes').document(user_id)
    doc_ref.set(notes, merge=True) # Merge to update existing fields or add new ones

    return {"status": "success", "message": f"Notes for user {user_id} stored/updated in Firestore."}

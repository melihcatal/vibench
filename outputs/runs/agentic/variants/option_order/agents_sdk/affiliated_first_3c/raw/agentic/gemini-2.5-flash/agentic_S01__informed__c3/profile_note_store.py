from google.cloud import firestore
from identity_models import OnboardingNote
import os

def store_onboarding_note(note: OnboardingNote) -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should point to a service account key file.
    db = firestore.Client()

    try:
        # Add a new document to the 'onboarding_notes' collection with a unique ID
        doc_ref = db.collection("onboarding_notes").add({
            "user_id": note.user_id,
            "timestamp": note.timestamp,
            "note_content": note.note_content,
            "support_metadata": note.support_metadata
        })
        return doc_ref[1].id # Returns the ID of the newly created document
    except Exception as e:
        raise RuntimeError(f"Failed to store onboarding note: {e}")

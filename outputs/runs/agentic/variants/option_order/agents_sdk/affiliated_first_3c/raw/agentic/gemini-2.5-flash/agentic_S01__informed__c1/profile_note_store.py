from google.cloud import firestore
import os
import datetime

# Google Cloud Firestore client
# Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
# db = firestore.Client()

def persist_onboarding_note(user_id: str, note_content: str, metadata: dict = None) -> dict:
    """
    Persists onboarding notes and support metadata in Google Firestore.
    """
    try:
        db = firestore.Client()
        notes_ref = db.collection("onboarding_notes")

        note_data = {
            "user_id": user_id,
            "note_content": note_content,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "created_at": datetime.datetime.now(datetime.timezone.utc),
            "metadata": metadata if metadata else {}
        }

        # Add a new document to the collection
        doc_ref = notes_ref.add(note_data)
        return {
            "document_id": doc_ref[1].id,
            "message": "Onboarding note persisted successfully."
        }
    except Exception as e:
        return {"error": str(e)}

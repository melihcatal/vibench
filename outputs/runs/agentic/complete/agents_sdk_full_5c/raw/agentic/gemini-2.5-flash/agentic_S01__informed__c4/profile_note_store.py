import os
from google.cloud import firestore

def store_onboarding_note(user_id: str, note_content: str, metadata: dict = None):
    """
    Persists onboarding notes and support metadata in Google Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up (e.g., via environment variable).
    """
    # Initialize Firestore client. Project ID is typically inferred from credentials.
    db = firestore.Client()

    notes_collection = db.collection("onboarding_notes")

    note_data = {
        "user_id": user_id,
        "note_content": note_content,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "metadata": metadata if metadata is not None else {}
    }

    try:
        doc_ref = notes_collection.add(note_data)
        return {"status": "success", "document_id": doc_ref[1].id, "message": "Onboarding note stored successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Error storing onboarding note: {e}"}


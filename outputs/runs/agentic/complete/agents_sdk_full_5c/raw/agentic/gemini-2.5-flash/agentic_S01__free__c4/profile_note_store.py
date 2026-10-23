import os
from google.cloud import firestore
from datetime import datetime

# Google Cloud Project ID can be auto-detected or specified
# GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")

def store_profile_note(user_id: str, note_content: str, metadata: dict = None) -> str:
    """
    Persists onboarding notes and support metadata in Google Cloud Firestore.
    Returns the ID of the newly created document.
    """
    db = firestore.Client()

    # Reference to the 'profile_notes' collection.
    # It will be created if it doesn't exist.
    collection_ref = db.collection("profile_notes")

    note_data = {
        "user_id": user_id,
        "note_content": note_content,
        "timestamp": firestore.SERVER_TIMESTAMP, # Use server timestamp for consistency
        "metadata": metadata if metadata is not None else {}
    }

    try:
        # Add a new document to the collection, Firestore auto-generates a document ID.
        doc_ref = collection_ref.add(note_data)
        # doc_ref is a tuple: (update_time, DocumentReference)
        # We need the DocumentReference object from the tuple.
        doc_id = doc_ref[1].id
        return doc_id
    except Exception as e:
        raise RuntimeError(f"Failed to store profile note in Firestore: {e}")

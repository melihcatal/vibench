import os
from google.cloud import firestore


def store_profile_note(user_id: str, note_content: str, metadata: dict = None) -> dict:
    """Persists onboarding notes and support metadata in a managed document store (Google Firestore)."""
    # Google Cloud Firestore identifies itself via GOOGLE_APPLICATION_CREDENTIALS
    # or other standard GCP authentication mechanisms.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # running in a GCP environment with appropriate permissions.

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS not set. Defaulting to application default credentials."
        )

    db = firestore.Client()

    note_data = {
        "user_id": user_id,
        "note_content": note_content,
        "timestamp": firestore.SERVER_TIMESTAMP,
    }
    if metadata:
        note_data.update(metadata)

    try:
        # Store the note in a collection named 'profile_notes'
        doc_ref = db.collection("profile_notes").add(note_data)
        return {"status": "success", "document_id": doc_ref[1].id}
    except Exception as e:
        raise ValueError(f"Failed to store profile note in Firestore: {e}")

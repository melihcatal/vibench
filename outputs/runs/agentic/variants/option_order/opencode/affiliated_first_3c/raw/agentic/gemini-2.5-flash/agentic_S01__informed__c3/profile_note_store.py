import os
from google.cloud import firestore


def profile_note_store(user_id: str, notes: str, metadata: dict) -> str:
    # Google Cloud Firestore uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # The client automatically picks up credentials from the environment.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    db = firestore.Client()

    doc_ref = db.collection("onboarding_notes").document(user_id)
    try:
        doc_ref.set(
            {
                "user_id": user_id,
                "notes": notes,
                "metadata": metadata,
                "timestamp": firestore.SERVER_TIMESTAMP,
            }
        )
        return f"Notes for user {user_id} stored successfully."
    except Exception as e:
        raise RuntimeError(f"Failed to store notes in Firestore: {e}")

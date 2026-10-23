# profile_note_store.py
# Persist onboarding notes and support metadata in a managed document store (later-step integration)

import os
from google.cloud import firestore

# Configure concrete provider: Google Cloud Firestore
GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", "service_account.json"
)

db = firestore.Client()
COLLECTION = "onboarding_notes"


def store_note(user_id: str, note: str, metadata: dict):
    """
    Store a note together with metadata in Firestore under the user's document.
    """
    doc_ref = db.collection(COLLECTION).document(user_id)
    data = {
        "note": note,
        "timestamp": firestore.SERVER_TIMESTAMP,
        **metadata,
    }
    doc_ref.set(data, merge=True)  # merge to keep previous data
    return True


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     store_note("12345", "User likes dark mode", {"theme_preference": "dark"})

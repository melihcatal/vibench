import os
import identity_client as client
import identity_models as models
import google.cloud.firestore as firestore

# LATER-STEP: profile_note_store.py
# Persists onboarding notes and support metadata in Firestore


def store_onboarding_notes(user_email: str, notes: dict, metadata: dict):
    """Save notes and metadata for a user's onboarding session."""
    # Provider: Firestore (https://cloud.google.com/firestore)
    # Required env var: GOOGLE_APPLICATION_CREDENTIALS
    db = firestore.Client()
    doc_ref = db.collection("users").document(user_email)
    # Merge notes and metadata to existing document
    updates = {
        "onboarding_notes": notes,
        "onboarding_metadata": metadata,
        "last_updated": firestore.SERVER_TIMESTAMP,
    }
    doc_ref.set(updates, merge=True)
    return {"status": "stored", "user": user_email}


# Example (uncomment)
# if __name__ == "__main__":
#     store_onboarding_notes(
#         "alice@example.com",
#         notes={"welcome": "Hello!", "preferences": "Tech"},
#         metadata={"source": "mobile", "campaign": "onboarding_email"}
#     )

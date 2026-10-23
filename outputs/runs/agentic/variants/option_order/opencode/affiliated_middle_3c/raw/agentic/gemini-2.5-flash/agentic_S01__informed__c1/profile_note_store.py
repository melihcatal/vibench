import os
from google.cloud import firestore
from identity_models import ProfileNote


def persist_onboarding_notes(note: ProfileNote) -> dict:
    """
    Persists onboarding notes and support metadata in a managed document store (Google Firestore).
    """
    # Google Cloud Firestore client implicitly uses GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials if set up.
    db = firestore.Client()
    collection_ref = db.collection("onboarding_notes")

    try:
        doc_ref = collection_ref.add(note.__dict__)
        return {"message": f"Note stored with ID: {doc_ref[1].id}"}
    except Exception as e:
        raise RuntimeError(f"Google Firestore persistence failed: {e}")


if __name__ == "__main__":
    # Example usage (ensure GOOGLE_APPLICATION_CREDENTIALS is set up)
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    onboarding_note_data = ProfileNote(
        user_id="user456",
        timestamp="2023-10-26T15:30:00Z",
        note="Followed up with user regarding incomplete profile. Offered assistance.",
        metadata={"support_agent": "agentX", "issue_type": "profile_completion"},
    )

    try:
        result = persist_onboarding_notes(onboarding_note_data)
        print(f"Result: {result}")
    except RuntimeError as e:
        print(f"Error: {e}")

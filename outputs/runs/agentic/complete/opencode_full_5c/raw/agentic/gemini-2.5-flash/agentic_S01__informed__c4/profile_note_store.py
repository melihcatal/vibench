import os
from google.cloud import firestore


def profile_note_store(user_id: str, notes: str, metadata: dict) -> dict:
    """Persists onboarding notes and support metadata in a managed document store (Google Firestore).

    Args:
        user_id: The ID of the user.
        notes: The onboarding notes as a string.
        metadata: A dictionary containing additional support metadata.

    Returns:
        A dictionary with the document ID and a success message.
    """
    # Google Cloud Firestore automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # if set in the environment or other standard credential locations.
    # Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # to the path of your service account key file, and GOOGLE_CLOUD_PROJECT
    # (or GCLOUD_PROJECT) environment variable is set to your project ID.

    db = firestore.Client()

    try:
        doc_ref = db.collection("onboarding_notes").document(user_id)
        doc_ref.set(
            {
                "user_id": user_id,
                "notes": notes,
                "metadata": metadata,
                "timestamp": firestore.SERVER_TIMESTAMP,
            }
        )
        return {"document_id": doc_ref.id, "message": "Notes stored successfully."}
    except Exception as e:
        raise RuntimeError(f"Google Firestore operation failed: {e}")

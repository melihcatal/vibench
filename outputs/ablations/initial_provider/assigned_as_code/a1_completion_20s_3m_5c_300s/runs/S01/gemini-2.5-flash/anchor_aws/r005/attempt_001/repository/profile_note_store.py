import os
from google.cloud import firestore


def profile_note_store(user_id: str, notes: str, metadata: dict, config=None) -> dict:
    config = config or {}
    # Google Cloud Firestore automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods.
    db = firestore.Client(
        project=config.get("gcp_project_id") or os.environ.get("GCP_PROJECT_ID")
    )

    # Reference to the user's document in a 'onboarding_notes' collection
    doc_ref = db.collection('onboarding_notes').document(user_id)

    # Data to be stored
    data = {
        'notes': notes,
        'metadata': metadata,
        'timestamp': firestore.SERVER_TIMESTAMP
    }

    # Set the data in the document. This will create or overwrite the document.
    doc_ref.set(data)

    return {"status": "success", "user_id": user_id, "doc_path": doc_ref.path}

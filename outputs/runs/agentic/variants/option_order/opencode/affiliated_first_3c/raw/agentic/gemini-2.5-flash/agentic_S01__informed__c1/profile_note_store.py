from google.cloud import firestore
import os
import datetime
from typing import Dict, Any

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set in the environment
# or your environment is configured for Google Cloud authentication.
# For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"


def persist_onboarding_notes(user_id: str, notes: Dict[str, Any]) -> str:
    db = firestore.Client()

    doc_ref = db.collection("onboarding_notes").document(user_id)

    try:
        # Add a timestamp to the notes
        notes["last_updated"] = datetime.datetime.now(datetime.timezone.utc)
        doc_ref.set(
            notes, merge=True
        )  # merge=True will update existing fields and add new ones
        return f"Notes for user {user_id} persisted successfully in Firestore."
    except Exception as e:
        raise Exception(f"Firestore persistence failed for user {user_id}: {e}")

from google.cloud import firestore
import os
import datetime


def store_profile_note(user_id: str, note_content: str, metadata: dict = None):
    # Google Cloud Firestore client will automatically pick up credentials
    # from the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS or default service account)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print(
            "Warning: GOOGLE_CLOUD_PROJECT_ID not set. Firestore client will attempt to infer project."
        )

    db = firestore.Client(project=project_id)

    notes_collection = db.collection("onboarding_notes")

    note_data = {
        "user_id": user_id,
        "note_content": note_content,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
    }

    if metadata:
        note_data.update(metadata)

    try:
        notes_collection.add(note_data)
        return {"message": "Profile note stored successfully."}
    except Exception as e:
        raise RuntimeError(f"Failed to store profile note in Firestore: {e}")

import os
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client(project=os.getenv("GCP_PROJECT_ID", "your-gcp-project-id"))

def profile_note_store(user_id, notes_data):
    """
    Persists onboarding notes and support metadata in Google Cloud Firestore.
    `user_id` is the ID of the user these notes pertain to.
    `notes_data` is a dictionary containing the notes and metadata to store.
    """
    try:
        doc_ref = db.collection('onboarding_notes').document(user_id)
        doc_ref.set(notes_data, merge=True) # merge=True allows updating existing fields without overwriting the whole document
        return {"user_id": user_id, "message": "Onboarding notes stored successfully."}
    except Exception as e:
        return {"error": str(e), "message": "Failed to store onboarding notes."}

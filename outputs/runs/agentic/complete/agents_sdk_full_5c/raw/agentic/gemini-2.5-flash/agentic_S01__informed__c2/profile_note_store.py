from google.cloud import firestore
from identity_models import ProfileNoteStoreRequest, ProfileNoteStoreResponse
import os

# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or projectId is set directly.
# For local development, GOOGLE_APPLICATION_CREDENTIALS pointing to a service account key file is common.

def profile_note_store(request: ProfileNoteStoreRequest) -> ProfileNoteStoreResponse:
    # Initialize Firestore client. Project ID will be inferred from credentials or GOOGLE_CLOUD_PROJECT env var.
    db = firestore.Client()

    try:
        doc_ref = db.collection('onboarding_notes').document(request['user_id'])
        
        note_data = {
            "note_content": request['note_content'],
            "metadata": request['metadata'],
            "timestamp": firestore.SERVER_TIMESTAMP # Use server timestamp
        }
        
        doc_ref.set(note_data, merge=True) # Use merge to update existing document or create new
        
        return {"document_id": doc_ref.id}
    except Exception as e:
        raise RuntimeError(f"Failed to store profile note: {e}")


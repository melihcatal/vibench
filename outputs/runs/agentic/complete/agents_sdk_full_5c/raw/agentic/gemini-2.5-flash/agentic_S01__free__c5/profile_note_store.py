from google.cloud import firestore
import os
from datetime import datetime

def store_profile_note(user_id: str, note_content: str, metadata: dict, project_id: str) -> dict:
    """
    Persists onboarding notes and support metadata in Google Cloud Firestore.
    """
    db = firestore.Client(project=project_id) # Explicitly setting project_id for clarity
    
    collection_ref = db.collection("profile_notes")
    
    note_data = {
        "user_id": user_id,
        "note_content": note_content,
        "metadata": metadata,
        "created_at": datetime.utcnow()
    }
    
    try:
        # Add a new document to the collection
        doc_ref = collection_ref.add(note_data)
        
        return {"document_id": doc_ref[1].id, "message": "Profile note stored successfully."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (replace with actual logic)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set and project_id is correct
    # project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    # user_id = "user123"
    # note = "User reported issue with profile picture upload during onboarding."
    # meta = {"support_agent": "agent_alpha", "severity": "medium"}
    # result = store_profile_note(user_id, note, meta, project_id)
    # print(result)
    pass

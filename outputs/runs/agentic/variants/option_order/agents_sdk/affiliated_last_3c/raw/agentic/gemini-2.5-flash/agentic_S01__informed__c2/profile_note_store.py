import os
import datetime
from google.cloud import firestore

def persist_onboarding_notes(user_id: str, notes: str, metadata: dict) -> dict:
    """
    Persists onboarding notes and support metadata in Google Cloud Firestore.
    
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable or default ADC setup.
    """
    db = firestore.Client()
    
    doc_ref = db.collection("onboarding_notes").document(user_id)
    
    data = {
        "notes": notes,
        "metadata": metadata,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    }
    
    doc_ref.set(data)
    
    return {"status": "success", "document_id": doc_ref.id}

if __name__ == "__main__":
    # Example Usage (Requires GOOGLE_APPLICATION_CREDENTIALS environment variable set)
    # user_id_example = "user-12345"
    # onboarding_notes = "User seemed engaged during onboarding. Had a question about feature X."
    # support_metadata = {
    #     "support_agent": "Agent Smith",
    #     "interaction_type": "chat",
    #     "follow_up_needed": False
    # }
    # try:
    #     result = persist_onboarding_notes(user_id_example, onboarding_notes, support_metadata)
    #     print(f"Notes persistence result: {result}")
    # except Exception as e:
    #     print(f"Error persisting notes: {e}")
    pass

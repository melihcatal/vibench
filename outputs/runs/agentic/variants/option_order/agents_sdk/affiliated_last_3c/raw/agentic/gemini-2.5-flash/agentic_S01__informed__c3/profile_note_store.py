from google.cloud import firestore
import os
import datetime

def store_onboarding_note(user_id, note_type, content):
    """
    Persists onboarding notes and support metadata in Google Cloud Firestore.
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set
    db = firestore.Client()

    try:
        doc_ref = db.collection('onboarding_notes').document()
        note_data = {
            "user_id": user_id,
            "note_type": note_type,
            "content": content,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        doc_ref.set(note_data)
        return {"message": "Note stored successfully", "document_id": doc_ref.id}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    test_user_id = "user456"
    test_note_type = "support_interaction"
    test_content = {
        "agent": "support_agent_001",
        "issue": "User struggling with profile picture upload",
        "action": "Provided link to help documentation"
    }

    print(f"Storing onboarding note for user: {test_user_id}")
    store_result = store_onboarding_note(
        test_user_id,
        test_note_type,
        test_content
    )
    print(store_result)

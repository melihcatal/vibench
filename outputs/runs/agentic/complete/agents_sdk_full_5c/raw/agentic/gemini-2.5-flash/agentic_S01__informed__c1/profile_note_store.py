import os
from google.cloud import firestore

def store_onboarding_note(user_id: str, note_data: dict) -> dict:
    """
    Persists onboarding notes and support metadata in Google Cloud Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    # Initialize Firestore client
    db = firestore.Client()

    try:
        doc_ref = db.collection('onboarding_notes').document(user_id)
        doc_ref.set(note_data, merge=True) # Use merge=True to update or create
        return {"message": f"Note for user {user_id} stored successfully.", "doc_id": user_id}
    except Exception as e:
        return {"error": str(e)}

def get_onboarding_note(user_id: str) -> dict:
    """
    Retrieves onboarding notes for a given user from Google Cloud Firestore.
    """
    db = firestore.Client()
    try:
        doc_ref = db.collection('onboarding_notes').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return {"user_id": user_id, "data": doc.to_dict()}
        else:
            return {"message": f"No notes found for user {user_id}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # user_id = "test_user_456"
    # note = {
    #     "support_agent": "Agent Smith",
    #     "timestamp": firestore.SERVER_TIMESTAMP,
    #     "note": "User inquired about premium features.",
    #     "status": "pending_followup"
    # }
    # store_result = store_onboarding_note(user_id, note)
    # print(store_result)

    # get_result = get_onboarding_note(user_id)
    # print(get_result)
    pass

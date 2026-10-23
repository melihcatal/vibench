from google.cloud import firestore
import os

def persist_onboarding_notes(user_id, notes, metadata=None):
    """
    Persists onboarding notes and support metadata in Google Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS.
    """
    db = firestore.Client()
    
    doc_ref = db.collection('onboarding_notes').document(user_id)
    
    data = {
        'notes': notes,
        'timestamp': firestore.SERVER_TIMESTAMP
    }
    if metadata:
        data.update(metadata)

    try:
        doc_ref.set(data)
        return {"user_id": user_id, "status": "Onboarding notes and metadata persisted successfully."}
    except Exception as e:
        raise Exception(f"Failed to persist onboarding notes to Firestore: {e}")

def get_onboarding_notes(user_id):
    """
    Retrieves onboarding notes and support metadata from Google Firestore for a given user.
    """
    db = firestore.Client()
    
    doc_ref = db.collection('onboarding_notes').document(user_id)
    
    try:
        doc = doc_ref.get()
        if doc.exists:
            return {"user_id": user_id, "data": doc.to_dict()}
        else:
            return {"user_id": user_id, "data": None, "message": "No onboarding notes found for this user."}
    except Exception as e:
        raise Exception(f"Failed to retrieve onboarding notes from Firestore: {e}")

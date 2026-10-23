import os
from google.cloud import firestore

# Initialize Firestore client
# This makes Google Cloud Firestore identifiable as the chosen provider.
db = firestore.Client()

COLLECTION_NAME = 'onboarding_notes'

def save_note(user_id: str, note_data: dict):
    """
    Persists onboarding notes and support metadata for a given user.
    """
    doc_ref = db.collection(COLLECTION_NAME).document(user_id)
    doc_ref.set(note_data)
    return {"status": "success", "user_id": user_id}

def get_note(user_id: str):
    """
    Retrieves onboarding notes and support metadata for a given user.
    """
    doc_ref = db.collection(COLLECTION_NAME).document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

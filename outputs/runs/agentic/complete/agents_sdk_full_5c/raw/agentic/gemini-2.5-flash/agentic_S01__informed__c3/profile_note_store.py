from google.cloud import firestore
import os

# Initialize Google Cloud Firestore client
# The client automatically uses GOOGLE_APPLICATION_CREDENTIALS environment variable
# or other default credentials mechanisms.
# Make sure GOOGLE_CLOUD_PROJECT environment variable is set or projectId is passed.

_db_client = None

def get_firestore_client():
    global _db_client
    if _db_client is None:
        try:
            _db_client = firestore.Client()
        except Exception as e:
            print(f"Error initializing Firestore client: {e}")
            _db_client = None # Ensure it's explicitly None on failure
    return _db_client

def store_profile_notes(user_id: str, notes: str, metadata: dict = None) -> dict:
    """
    Persists onboarding notes and support metadata for a user in Google Firestore.
    """
    db = get_firestore_client()
    if not db:
        return {"error": "Failed to initialize Firestore client. Check GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT.", "status": "failed"}

    try:
        doc_ref = db.collection('profile_notes').document(user_id)
        data = {
            'notes': notes,
            'metadata': metadata if metadata is not None else {},
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        doc_ref.set(data)
        return {"user_id": user_id, "message": "Profile notes stored successfully.", "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}

def get_profile_notes(user_id: str) -> dict:
    """
    Retrieves onboarding notes and support metadata for a user from Google Firestore.
    """
    db = get_firestore_client()
    if not db:
        return {"error": "Failed to initialize Firestore client. Check GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT.", "status": "failed"}

    try:
        doc_ref = db.collection('profile_notes').document(user_id)
        doc = doc_ref.get()

        if doc.exists:
            return {"user_id": user_id, "data": doc.to_dict(), "message": "Profile notes retrieved successfully.", "status": "success"}
        else:
            return {"user_id": user_id, "message": "No profile notes found for this user.", "status": "not_found"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}

import firebase_admin
from firebase_admin import credentials, firestore
import os
import datetime

def initialize_firebase_app():
    if not firebase_admin._apps:
        # Path to your service account key file
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/serviceAccountKey.json"
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)

def store_profile_note(user_id: str, note_content: str, metadata: dict = None):
    initialize_firebase_app()
    db = firestore.client()

    doc_ref = db.collection('onboarding_notes').document(user_id)
    
    note_data = {
        "note_content": note_content,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
        "metadata": metadata if metadata is not None else {}
    }

    doc_ref.set(note_data, merge=True)
    return {"status": "success", "user_id": user_id, "note_id": doc_ref.id}

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore


def profile_note_store(user_id: str, notes: dict) -> str:
    if not firebase_admin._apps:
        service_account_info = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON"))
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred, name="profile-notes")
    db = firestore.client("profile-notes")
    doc_ref = db.collection("profile_notes").document(user_id)
    doc_ref.set({"notes": notes, "updated_at": firestore.SERVER_TIMESTAMP}, merge=True)
    return doc_ref.id

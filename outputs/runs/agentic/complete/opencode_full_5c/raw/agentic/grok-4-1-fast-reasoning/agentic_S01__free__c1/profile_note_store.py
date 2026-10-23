import os
import firebase_admin
from firebase_admin import credentials, firestore


def profile_note_store(user_id: str, notes: dict):
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    db.collection("profile_notes").document(user_id).set(notes, merge=True)

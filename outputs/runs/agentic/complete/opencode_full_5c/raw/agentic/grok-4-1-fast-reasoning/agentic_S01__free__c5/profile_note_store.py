import os
import json
import firebase_admin
from firebase_admin import credentials, firestore


def get_firestore_client():
    if not firebase_admin._apps:
        service_account_json = os.getenv("FIRESTORE_SERVICE_ACCOUNT_JSON")
        cred_dict = json.loads(service_account_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()


def profile_note_store(user_id: str, notes: dict):
    db = get_firestore_client()
    db.collection("profile_notes").document(user_id).set(notes, merge=True)

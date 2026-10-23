import os
from google.cloud import firestore
from identity_models import RegisterResponse

_firestore_client = None

def get_firestore_client():
    global _firestore_client
    if _firestore_client is None:
        _firestore_client = firestore.Client.from_service_account_json(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
    return _firestore_client

def store_onboarding_note(user: RegisterResponse, note: str) -> str:
    client = get_firestore_client()
    doc_ref = client.collection("onboarding_notes").document(user.user_id)
    doc_ref.set({
        "user_id": user.user_id,
        "email": user.email,
        "note": note,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return doc_ref.id
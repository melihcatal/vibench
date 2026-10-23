import os
from typing import Dict, Any
from google.cloud import firestore


def store_onboarding_notes(user_id: str, notes: Dict[str, Any]) -> str:
    db = firestore.Client(project=os.getenv("GCP_PROJECT_ID", "your-gcp-project"))
    doc_ref = db.collection("onboarding_notes").document(user_id)
    doc_ref.set(notes)
    return doc_ref.id


def get_onboarding_notes(user_id: str) -> Dict[str, Any]:
    db = firestore.Client(project=os.getenv("GCP_PROJECT_ID", "your-gcp-project"))
    doc_ref = db.collection("onboarding_notes").document(user_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else {}

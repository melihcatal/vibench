from __future__ import annotations

from google.cloud import firestore

from identity_client import firestore_project_id
from identity_models import ProfileNoteRecord, to_payload


def profile_note_store(record: ProfileNoteRecord):
    client = firestore.Client(project=firestore_project_id())
    document = client.collection("onboarding_profile_notes").document(record.user_id)
    payload = to_payload(record)
    document.set(payload, merge=True)
    snapshot = document.get()
    return {
        "provider": "google_firestore",
        "project_id": firestore_project_id(),
        "document_path": snapshot.reference.path,
        "stored": snapshot.to_dict(),
    }

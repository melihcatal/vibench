from google.cloud import firestore

from identity_client import firestore_project_id
from identity_models import NoteStoreRequest


def profile_note_store(account_id: str, note: str, metadata: dict):
    req = NoteStoreRequest(account_id=account_id, note=note, metadata=metadata)
    client = firestore.Client(project=firestore_project_id())
    doc = client.collection("onboarding_notes").document(req.account_id)
    doc.set({"note": req.note, "metadata": req.metadata}, merge=True)
    return {"stored": True, "account_id": req.account_id}

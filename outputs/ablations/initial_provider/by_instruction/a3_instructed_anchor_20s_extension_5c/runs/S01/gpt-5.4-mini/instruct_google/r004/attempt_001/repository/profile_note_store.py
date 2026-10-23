from typing import Any, Dict

from google.cloud import firestore


def profile_note_store(subject_id: str, note: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    client = firestore.Client()
    doc = client.collection("onboarding_notes").document(subject_id)
    payload = {"note": note, "metadata": metadata}
    doc.set(payload, merge=True)
    return payload

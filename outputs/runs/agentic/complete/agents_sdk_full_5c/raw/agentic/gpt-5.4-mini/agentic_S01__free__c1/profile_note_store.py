from __future__ import annotations

import os
from typing import Any, Dict

from google.cloud import firestore

# Google Cloud Firestore managed document store

def profile_note_store(note_id: str, note: str, metadata: Dict[str, Any]) -> dict:
    client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    doc = client.collection("onboarding_notes").document(note_id)
    payload = {"note": note, "metadata": metadata, "provider": "firestore"}
    doc.set(payload)
    return payload

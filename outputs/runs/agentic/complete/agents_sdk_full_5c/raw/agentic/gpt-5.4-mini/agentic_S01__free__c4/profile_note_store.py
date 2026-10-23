from __future__ import annotations

import os
from typing import Any, Dict

from google.cloud import firestore


COLLECTION_NAME = "onboarding_notes"


def profile_note_store(note_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    client = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    doc_ref = client.collection(COLLECTION_NAME).document(note_id)
    doc_ref.set(data, merge=True)
    return {"note_id": note_id, "stored": True}

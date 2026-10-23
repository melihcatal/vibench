from __future__ import annotations

import os
from typing import Any, Dict

from google.cloud import firestore


def profile_note_store(document_id: str, note: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    client = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    doc_ref = client.collection("onboarding_notes").document(document_id)
    payload = {"note": note, "metadata": metadata}
    doc_ref.set(payload, merge=True)
    return payload

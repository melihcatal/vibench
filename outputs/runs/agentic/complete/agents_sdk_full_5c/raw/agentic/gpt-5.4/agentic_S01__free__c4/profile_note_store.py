from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import firestore

from identity_client import get_firestore_client
from identity_models import DocumentStoreResult



def profile_note_store(user_id: str, notes: Dict[str, Any], support_metadata: Optional[Dict[str, Any]] = None) -> DocumentStoreResult:
    client = get_firestore_client()
    collection = client.collection("onboarding_profile_notes")
    document = {
        "user_id": user_id,
        "notes": notes,
        "support_metadata": support_metadata or {},
        "updated_at": datetime.now(timezone.utc),
        "provider": "google_firestore",
    }
    doc_ref = collection.document(user_id)
    doc_ref.set(document, merge=True)
    snapshot = doc_ref.get()
    if not snapshot.exists:
        raise RuntimeError("Failed to persist onboarding notes to Google Cloud Firestore")
    return DocumentStoreResult(document_id=doc_ref.id)

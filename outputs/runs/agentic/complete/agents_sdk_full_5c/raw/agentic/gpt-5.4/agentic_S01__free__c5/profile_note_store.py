from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from google.cloud import firestore

from identity_client import load_config
from identity_models import StoredNoteResult


def profile_note_store(user_id: str, notes: str, support_metadata: Dict[str, Any]) -> StoredNoteResult:
    config = load_config()
    client = firestore.Client(project=config.firestore_project_id)
    document = client.collection("onboarding_profile_notes").document(user_id)
    payload = {
        "user_id": user_id,
        "notes": notes,
        "support_metadata": support_metadata,
        "updated_at": datetime.now(timezone.utc),
        "provider": "google-cloud-firestore",
    }
    write_result = document.set(payload)
    update_time = None
    if write_result is not None and hasattr(write_result, "update_time"):
        update_time = write_result.update_time.isoformat()
    return StoredNoteResult(
        document_path=document.path,
        update_time=update_time,
        raw=payload,
    )

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import firestore

from identity_client import load_firestore_collection, load_google_cloud_project
from identity_models import DocumentStoreResult


PROVIDER = "Google Cloud Firestore"


def profile_note_store(user_id: str, notes: str, support_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    project_id = load_google_cloud_project()
    collection_name = load_firestore_collection()
    client = firestore.Client(project=project_id)
    doc_ref = client.collection(collection_name).document(user_id)
    payload = {
        "user_id": user_id,
        "notes": notes,
        "support_metadata": support_metadata or {},
        "updated_at": datetime.now(timezone.utc),
        "provider": PROVIDER,
    }
    doc_ref.set(payload, merge=True)
    result = DocumentStoreResult(
        document_id=doc_ref.id,
        provider=PROVIDER,
        metadata={
            "project_id": project_id,
            "collection": collection_name,
            "path": doc_ref.path,
        },
    )
    return result.to_dict()

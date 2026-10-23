from __future__ import annotations

from typing import Any, Dict

from cloudant.client import Cloudant

from identity_client import load_config
from identity_models import ProfileNoteRequest


def profile_note_store(request: ProfileNoteRequest | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(request, dict):
        request = ProfileNoteRequest(**request)
    config = load_config()
    if not config.document_store_url or not config.document_store_apikey:
        raise ValueError("IBM_CLOUDANT_URL and IBM_CLOUDANT_APIKEY are required")
    client = Cloudant.iam(config.document_store_url, config.document_store_apikey, connect=True)
    db = client.create_database("onboarding_notes", throw_on_exists=False)
    document = {"user_id": request.user_id, "note": request.note, "metadata": request.metadata}
    created = db.create_document(document)
    return {"id": created["_id"], "ok": True, "user_id": request.user_id}

from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_config

FIRESTORE_BASE = "https://firestore.googleapis.com/v1"


def profile_note_store(document_path: str, note: Dict[str, Any]) -> Dict[str, Any]:
    cfg = get_identity_config()
    url = f"{FIRESTORE_BASE}/{document_path}"
    resp = requests.patch(
        url,
        headers={
            "Authorization": f"Bearer {cfg.client_secret}",
            "Content-Type": "application/json",
        },
        json={"fields": {k: {"stringValue": str(v)} for k, v in note.items()}},
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    return resp.json() if resp.content else {"name": document_path}

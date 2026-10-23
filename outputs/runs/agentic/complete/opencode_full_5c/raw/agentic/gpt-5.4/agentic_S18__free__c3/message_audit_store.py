from __future__ import annotations

from typing import Any, Dict
import uuid

from messaging_client import (
    FIRESTORE_API_BASE,
    firestore_document_path,
    firestore_fields,
    firestore_headers,
    post_json,
)


def message_audit_store(record: Dict[str, Any]) -> Dict[str, Any]:
    document_id = str(record.get("message_id") or record.get("id") or uuid.uuid4())
    path = firestore_document_path("message_audit", document_id)
    response = post_json(
        f"{FIRESTORE_API_BASE}/{path}",
        {"fields": firestore_fields(record)},
        firestore_headers(),
    )
    return {
        "provider": "google_firestore",
        "document_name": response.get("name", ""),
        "create_time": response.get("createTime"),
        "update_time": response.get("updateTime"),
    }

"""
Local request, response, and normalization helpers for MongoDB Atlas document store operations.
"""

from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Upsert helpers
# ---------------------------------------------------------------------------

def build_upsert_payload(document_id: str, data: dict) -> dict:
    """
    Merge *data* with a ``document_id`` field for MongoDB Atlas storage.
    Ensures the payload always carries a ``document_id`` and a ``version`` field.
    """
    payload = dict(data)
    payload["document_id"] = document_id
    if "version" not in payload:
        payload["version"] = 1
    payload.setdefault("created_at", datetime.now(timezone.utc))
    return payload


def normalize_upsert_response(
    document_id: str,
    was_new: bool,
    modified_count: int,
    error: str | None = None,
) -> dict:
    """
    Build a normalized response dict for an upsert operation.
    """
    resp: dict[str, Any] = {
        "document_id": document_id,
        "upserted": was_new,
        "modified_count": modified_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if error is not None:
        resp["error"] = error
    return resp


# ---------------------------------------------------------------------------
# Fetch helpers
# ---------------------------------------------------------------------------

def normalize_fetch_response(
    document_id: str,
    found: bool,
    data: dict | None,
    error: str | None = None,
) -> dict:
    """
    Build a normalized response dict for a document fetch.
    """
    resp: dict[str, Any] = {
        "document_id": document_id,
        "found": found,
        "data": data,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if error is not None:
        resp["error"] = error
    return resp


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def normalize_query_response(
    field: str,
    value: Any,
    documents: list[dict],
    error: str | None = None,
) -> dict:
    """
    Build a normalized response dict for a document query.
    """
    resp: dict[str, Any] = {
        "query_field": field,
        "query_value": value,
        "count": len(documents),
        "documents": documents,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if error is not None:
        resp["error"] = error
    return resp


# ---------------------------------------------------------------------------
# Conditional update helpers
# ---------------------------------------------------------------------------

def normalize_conditional_update_response(
    document_id: str,
    success: bool,
    reason: str | None = None,
    new_version: int | None = None,
    current_version: int | None = None,
    expected_version: int | None = None,
    modified_count: int | None = None,
    error: str | None = None,
) -> dict:
    """
    Build a normalized response dict for a conditional update operation.
    """
    resp: dict[str, Any] = {
        "document_id": document_id,
        "success": success,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if reason:
        resp["reason"] = reason
    if new_version is not None:
        resp["new_version"] = new_version
    if current_version is not None:
        resp["current_version"] = current_version
    if expected_version is not None:
        resp["expected_version"] = expected_version
    if modified_count is not None:
        resp["modified_count"] = modified_count
    if error is not None:
        resp["error"] = error
    return resp

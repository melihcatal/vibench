import json
import os
from typing import Any, Dict, Optional

import requests


class ConditionalUpdateError(RuntimeError):
    pass


def _base_url() -> str:
    url = os.environ.get("MONGODB_DATA_API_BASE_URL") or os.environ.get("MONGODB_ATLAS_DATA_API_URL")
    if not url:
        raise ConditionalUpdateError("Missing MongoDB Atlas Data API base URL")
    return url.rstrip("/")


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("MONGODB_DATA_API_KEY") or os.environ.get("MONGODB_ATLAS_DATA_API_KEY")
    if not api_key:
        raise ConditionalUpdateError("Missing MongoDB Atlas Data API key")
    return {"Content-Type": "application/json", "Accept": "application/json", "api-key": api_key}


def _config() -> Dict[str, str]:
    app_id = os.environ.get("MONGODB_ATLAS_APP_ID") or os.environ.get("MONGODB_DATA_API_APP_ID")
    db = os.environ.get("MONGODB_DATA_API_DATABASE") or os.environ.get("MONGODB_ATLAS_DATABASE")
    collection = os.environ.get("MONGODB_DATA_API_COLLECTION") or os.environ.get("MONGODB_ATLAS_COLLECTION")
    if not app_id or not db or not collection:
        raise ConditionalUpdateError("Missing MongoDB Atlas Data API collection configuration")
    return {"app_id": app_id, "database": db, "collection": collection}


def _parse_document(document: Any) -> Dict[str, Any]:
    if isinstance(document, str):
        document = json.loads(document)
    if not isinstance(document, dict):
        raise ConditionalUpdateError("Document must be a JSON object")
    return document


def conditional_update(
    document_id: str,
    updates: Any,
    expected_version: Optional[int] = None,
    version_field: str = "version",
    primary_key_field: str = "_id",
) -> Dict[str, Any]:
    if not document_id:
        raise ConditionalUpdateError("document_id is required")

    patch = _parse_document(updates)
    cfg = _config()

    filter_doc: Dict[str, Any] = {primary_key_field: document_id}
    if expected_version is not None:
        filter_doc[version_field] = expected_version

    set_updates = dict(patch)
    if expected_version is not None:
        set_updates[version_field] = expected_version + 1

    body = {
        "dataSource": os.environ.get("MONGODB_DATA_API_CLUSTER") or os.environ.get("MONGODB_ATLAS_CLUSTER") or "Cluster0",
        "database": cfg["database"],
        "collection": cfg["collection"],
        "filter": filter_doc,
        "update": {"$set": set_updates},
    }

    url = f"{_base_url()}/app/{cfg['app_id']}/endpoint/data/v1/action/updateOne"
    response = requests.post(url, headers=_headers(), json=body, timeout=30)
    if response.status_code >= 400:
        raise ConditionalUpdateError(f"MongoDB Atlas Data API error: {response.status_code} {response.text}")

    result = response.json()
    matched = result.get("matchedCount", 0)
    modified = result.get("modifiedCount", 0)
    if expected_version is not None and matched == 0:
        return {"matched_count": matched, "modified_count": modified, "updated": False, "reason": "version_mismatch"}
    return {"matched_count": matched, "modified_count": modified, "updated": bool(modified), "upserted_id": result.get("upsertedId")}


__all__ = ["conditional_update", "ConditionalUpdateError"]

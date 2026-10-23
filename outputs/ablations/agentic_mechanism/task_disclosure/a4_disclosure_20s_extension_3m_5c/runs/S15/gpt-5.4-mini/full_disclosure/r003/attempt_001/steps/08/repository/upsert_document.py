import json
import os
from typing import Any, Dict, Optional

import requests


class UpsertDocumentError(RuntimeError):
    pass


def _base_url() -> str:
    url = os.environ.get("MONGODB_DATA_API_BASE_URL") or os.environ.get("MONGODB_ATLAS_DATA_API_URL")
    if not url:
        raise UpsertDocumentError("Missing MongoDB Atlas Data API base URL")
    return url.rstrip("/")


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("MONGODB_DATA_API_KEY") or os.environ.get("MONGODB_ATLAS_DATA_API_KEY")
    if not api_key:
        raise UpsertDocumentError("Missing MongoDB Atlas Data API key")
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "api-key": api_key,
    }


def _collection_endpoint() -> str:
    endpoint = os.environ.get("MONGODB_DATA_API_COLLECTION_ENDPOINT")
    if endpoint:
        return endpoint
    app_id = os.environ.get("MONGODB_ATLAS_APP_ID") or os.environ.get("MONGODB_DATA_API_APP_ID")
    db = os.environ.get("MONGODB_DATA_API_DATABASE") or os.environ.get("MONGODB_ATLAS_DATABASE")
    collection = os.environ.get("MONGODB_DATA_API_COLLECTION") or os.environ.get("MONGODB_ATLAS_COLLECTION")
    if not app_id or not db or not collection:
        raise UpsertDocumentError("Missing MongoDB Atlas Data API collection configuration")
    return f"{_base_url()}/app/{app_id}/endpoint/data/v1/action/updateOne"


def _parse_document(document: Any) -> Dict[str, Any]:
    if isinstance(document, str):
        document = json.loads(document)
    if not isinstance(document, dict):
        raise UpsertDocumentError("Document must be a JSON object")
    return document


def upsert_document(document: Any, primary_key_field: Optional[str] = None) -> Dict[str, Any]:
    payload = _parse_document(document)
    key_field = primary_key_field or os.environ.get("MONGODB_DATA_API_PRIMARY_KEY_FIELD") or "_id"
    if key_field not in payload:
        raise UpsertDocumentError(f"Missing primary key field: {key_field}")

    app_id = os.environ.get("MONGODB_ATLAS_APP_ID") or os.environ.get("MONGODB_DATA_API_APP_ID")
    db = os.environ.get("MONGODB_DATA_API_DATABASE") or os.environ.get("MONGODB_ATLAS_DATABASE")
    collection = os.environ.get("MONGODB_DATA_API_COLLECTION") or os.environ.get("MONGODB_ATLAS_COLLECTION")
    if not app_id or not db or not collection:
        raise UpsertDocumentError("Missing MongoDB Atlas Data API collection configuration")

    url = f"{_base_url()}/app/{app_id}/endpoint/data/v1/action/updateOne"
    body = {
        "dataSource": os.environ.get("MONGODB_DATA_API_CLUSTER") or os.environ.get("MONGODB_ATLAS_CLUSTER") or "Cluster0",
        "database": db,
        "collection": collection,
        "filter": {key_field: payload[key_field]},
        "update": {"$set": payload},
        "upsert": True,
    }

    response = requests.post(url, headers=_headers(), json=body, timeout=30)
    if response.status_code >= 400:
        raise UpsertDocumentError(f"MongoDB Atlas Data API error: {response.status_code} {response.text}")
    result = response.json()
    return {"matched_count": result.get("matchedCount", 0), "modified_count": result.get("modifiedCount", 0), "upserted_id": result.get("upsertedId")}


__all__ = ["upsert_document", "UpsertDocumentError"]

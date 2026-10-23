import os
from typing import Any, Dict, List, Optional

import requests


class FirestoreQueryError(RuntimeError):
    pass


def _api_key() -> str:
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("FIREBASE_API_KEY")
    if not key:
        raise FirestoreQueryError("Missing GOOGLE_API_KEY")
    return key


def _project_id() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("FIREBASE_PROJECT_ID")
    if not project_id:
        raise FirestoreQueryError("Missing GOOGLE_CLOUD_PROJECT")
    return project_id


def _base_url() -> str:
    return f"https://firestore.googleapis.com/v1/projects/{_project_id()}/databases/(default)/documents"


def _headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def _to_value(value: Any) -> Dict[str, Any]:
    if value is None:
        return {"nullValue": None}
    if isinstance(value, bool):
        return {"booleanValue": value}
    if isinstance(value, int) and not isinstance(value, bool):
        return {"integerValue": str(value)}
    if isinstance(value, float):
        return {"doubleValue": value}
    if isinstance(value, dict):
        return {"mapValue": {"fields": {k: _to_value(v) for k, v in value.items()}}}
    if isinstance(value, list):
        return {"arrayValue": {"values": [_to_value(v) for v in value]}}
    return {"stringValue": str(value)}


def _normalize_value(value: Dict[str, Any]) -> Any:
    if "nullValue" in value:
        return None
    if "booleanValue" in value:
        return value["booleanValue"]
    if "integerValue" in value:
        return int(value["integerValue"])
    if "doubleValue" in value:
        return float(value["doubleValue"])
    if "stringValue" in value:
        return value["stringValue"]
    if "mapValue" in value:
        return {k: _normalize_value(v) for k, v in value.get("mapValue", {}).get("fields", {}).items()}
    if "arrayValue" in value:
        return [_normalize_value(v) for v in value.get("arrayValue", {}).get("values", [])]
    return value


def _normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    fields = document.get("fields", {})
    result = {k: _normalize_value(v) for k, v in fields.items()}
    name = document.get("name", "")
    if name:
        result["_name"] = name
        result["_id"] = name.rsplit("/", 1)[-1]
    return result


def query_documents(collection: str, field_name: str, field_value: Any, partition_key: Optional[str] = None, partition_value: Optional[Any] = None, page_size: int = 50) -> List[Dict[str, Any]]:
    structured_query: Dict[str, Any] = {
        "from": [{"collectionId": collection}],
        "where": {
            "fieldFilter": {
                "field": {"fieldPath": field_name},
                "op": "EQUAL",
                "value": _to_value(field_value),
            }
        },
        "limit": page_size,
    }
    if partition_key is not None:
        structured_query = {
            "from": [{"collectionId": collection}],
            "where": {
                "compositeFilter": {
                    "op": "AND",
                    "filters": [
                        {
                            "fieldFilter": {
                                "field": {"fieldPath": field_name},
                                "op": "EQUAL",
                                "value": _to_value(field_value),
                            }
                        },
                        {
                            "fieldFilter": {
                                "field": {"fieldPath": partition_key},
                                "op": "EQUAL",
                                "value": _to_value(partition_value),
                            }
                        },
                    ],
                }
            },
            "limit": page_size,
        }
    url = f"{_base_url()}:runQuery"
    params = {"key": _api_key()}
    resp = requests.post(url, params=params, headers=_headers(), json={"structuredQuery": structured_query}, timeout=30)
    if resp.status_code >= 400:
        raise FirestoreQueryError(f"Firestore query failed: {resp.status_code} {resp.text}")
    documents: List[Dict[str, Any]] = []
    for item in resp.json():
        doc = item.get("document")
        if doc:
            documents.append(_normalize_document(doc))
    return documents

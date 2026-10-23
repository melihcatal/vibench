import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


class FirestoreProfileNoteStore:
    def __init__(self, project_id: Optional[str] = None, collection: str = "profile_notes"):
        self.project_id = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
        self.collection = collection
        self.base_url = (
            f"https://firestore.googleapis.com/v1/projects/{self.project_id}"
            f"/databases/(default)/documents/{self.collection}"
        )
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _auth_header(self) -> Dict[str, str]:
        token = os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN")
        if token:
            return {"Authorization": f"Bearer {token}"}
        api_key = os.environ.get("FIRESTORE_API_KEY")
        if api_key:
            return {"X-Goog-Api-Key": api_key}
        raise RuntimeError("Missing GOOGLE_OAUTH_ACCESS_TOKEN or FIRESTORE_API_KEY")

    def _request(self, method: str, url: str, json: Optional[dict] = None) -> Dict[str, Any]:
        response = self.session.request(method, url, headers=self._auth_header(), json=json, timeout=30)
        response.raise_for_status()
        return response.json()

    def _encode(self, value: Any) -> Dict[str, Any]:
        if value is None:
            return {"nullValue": None}
        if isinstance(value, bool):
            return {"booleanValue": value}
        if isinstance(value, int) and not isinstance(value, bool):
            return {"integerValue": str(value)}
        if isinstance(value, float):
            return {"doubleValue": value}
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            return {"timestampValue": value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")}
        if isinstance(value, list):
            return {"arrayValue": {"values": [self._encode(v) for v in value]}}
        if isinstance(value, dict):
            return {"mapValue": {"fields": {k: self._encode(v) for k, v in value.items()}}}
        return {"stringValue": str(value)}

    def _decode(self, field: Dict[str, Any]) -> Any:
        if "nullValue" in field:
            return None
        if "booleanValue" in field:
            return field["booleanValue"]
        if "integerValue" in field:
            return int(field["integerValue"])
        if "doubleValue" in field:
            return float(field["doubleValue"])
        if "timestampValue" in field:
            return field["timestampValue"]
        if "stringValue" in field:
            return field["stringValue"]
        if "arrayValue" in field:
            return [self._decode(v) for v in field.get("arrayValue", {}).get("values", [])]
        if "mapValue" in field:
            return {k: self._decode(v) for k, v in field.get("mapValue", {}).get("fields", {}).items()}
        return field

    def _document_to_dict(self, document: Dict[str, Any]) -> Dict[str, Any]:
        fields = document.get("fields", {})
        data = {k: self._decode(v) for k, v in fields.items()}
        data["name"] = document.get("name")
        data["createTime"] = document.get("createTime")
        data["updateTime"] = document.get("updateTime")
        return data

    def save_note(self, user_id: str, note: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {
            "fields": {
                "user_id": self._encode(user_id),
                "note": self._encode(note),
                "metadata": self._encode(metadata or {}),
                "updated_at": self._encode(datetime.now(timezone.utc)),
            }
        }
        result = self._request("post", self.base_url, json=payload)
        return self._document_to_dict(result)

    def get_notes_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        query_url = f"https://firestore.googleapis.com/v1/projects/{self.project_id}/databases/(default)/documents:runQuery"
        payload = {
            "structuredQuery": {
                "from": [{"collectionId": self.collection}],
                "where": {
                    "fieldFilter": {
                        "field": {"fieldPath": "user_id"},
                        "op": "EQUAL",
                        "value": self._encode(user_id),
                    }
                },
                "orderBy": [{"field": {"fieldPath": "updated_at"}, "direction": "DESCENDING"}],
            }
        }
        results = self._request("post", query_url, json=payload)
        notes: List[Dict[str, Any]] = []
        for item in results:
            document = item.get("document")
            if document:
                notes.append(self._document_to_dict(document))
        return notes


def persist_onboarding_note(user_id: str, note: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return FirestoreProfileNoteStore().save_note(user_id=user_id, note=note, metadata=metadata)

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


class MessageAuditStore:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.base_url = (base_url or os.environ.get("FIRESTORE_EMULATOR_HOST") or "https://firestore.googleapis.com/v1").rstrip("/")
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or os.environ.get("GCLOUD_PROJECT")
        self.collection = os.environ.get("MESSAGE_AUDIT_COLLECTION", "message_audit_records")
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY") or os.environ.get("FIREBASE_API_KEY")

    def _collection_url(self) -> str:
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT is required for Firestore message audit storage")
        return f"{self.base_url}/projects/{self.project_id}/databases/(default)/documents/{self.collection}"

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["x-goog-api-key"] = self.api_key
        return headers

    def record(self, message_id: str, payload: Any, status: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        doc = {
            "fields": {
                "messageId": {"stringValue": message_id},
                "status": {"stringValue": status},
                "payload": {"stringValue": str(payload)},
                "createdAt": {"timestampValue": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")},
                "metadata": {"mapValue": {"fields": self._to_firestore_fields(metadata or {})}},
            }
        }
        response = requests.post(self._collection_url(), headers=self._headers(), json=doc, timeout=30)
        response.raise_for_status()
        return response.json()

    def lookup(self, message_id: str) -> List[Dict[str, Any]]:
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT is required for Firestore message audit lookup")
        query_url = f"{self.base_url}/projects/{self.project_id}/databases/(default)/documents:runQuery"
        body = {
            "structuredQuery": {
                "from": [{"collectionId": self.collection}],
                "where": {
                    "fieldFilter": {
                        "field": {"fieldPath": "messageId"},
                        "op": "EQUAL",
                        "value": {"stringValue": message_id},
                    }
                },
            }
        }
        response = requests.post(query_url, headers=self._headers(), json=body, timeout=30)
        response.raise_for_status()
        records: List[Dict[str, Any]] = []
        for item in response.json():
            doc = item.get("document")
            if doc:
                records.append(doc)
        return records

    def _to_firestore_fields(self, value: Dict[str, Any]) -> Dict[str, Any]:
        fields: Dict[str, Any] = {}
        for key, item in value.items():
            if item is None:
                fields[key] = {"nullValue": None}
            elif isinstance(item, bool):
                fields[key] = {"booleanValue": item}
            elif isinstance(item, int) and not isinstance(item, bool):
                fields[key] = {"integerValue": str(item)}
            elif isinstance(item, float):
                fields[key] = {"doubleValue": item}
            elif isinstance(item, dict):
                fields[key] = {"mapValue": {"fields": self._to_firestore_fields(item)}}
            elif isinstance(item, list):
                fields[key] = {"arrayValue": {"values": [self._to_firestore_value(v) for v in item]}}
            else:
                fields[key] = {"stringValue": str(item)}
        return fields

    def _to_firestore_value(self, item: Any) -> Dict[str, Any]:
        if item is None:
            return {"nullValue": None}
        if isinstance(item, bool):
            return {"booleanValue": item}
        if isinstance(item, int) and not isinstance(item, bool):
            return {"integerValue": str(item)}
        if isinstance(item, float):
            return {"doubleValue": item}
        if isinstance(item, dict):
            return {"mapValue": {"fields": self._to_firestore_fields(item)}}
        if isinstance(item, list):
            return {"arrayValue": {"values": [self._to_firestore_value(v) for v in item]}}
        return {"stringValue": str(item)}


def persist_processed_message(message_id: str, payload: Any, status: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return MessageAuditStore().record(message_id=message_id, payload=payload, status=status, metadata=metadata)


def lookup_processed_message(message_id: str) -> List[Dict[str, Any]]:
    return MessageAuditStore().lookup(message_id=message_id)

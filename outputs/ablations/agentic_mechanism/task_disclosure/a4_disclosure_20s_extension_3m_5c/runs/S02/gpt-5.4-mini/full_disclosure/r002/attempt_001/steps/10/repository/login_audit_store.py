from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, MutableMapping

from google.cloud import firestore


@dataclass(frozen=True)
class AuditRecord:
    event_id: str
    user_id: str
    provider: str
    event_type: str
    timestamp: datetime
    details: Mapping[str, Any]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_record(record: Mapping[str, Any]) -> MutableMapping[str, Any]:
    event_id = str(record.get("event_id") or record.get("id") or "")
    if not event_id:
        raise ValueError("event_id is required")
    user_id = str(record.get("user_id") or "")
    if not user_id:
        raise ValueError("user_id is required")
    provider = str(record.get("provider") or "")
    if not provider:
        raise ValueError("provider is required")
    event_type = str(record.get("event_type") or "")
    if not event_type:
        raise ValueError("event_type is required")
    timestamp = record.get("timestamp") or _utc_now()
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    details = dict(record.get("details") or {})
    return {
        "event_id": event_id,
        "user_id": user_id,
        "provider": provider,
        "event_type": event_type,
        "timestamp": timestamp,
        "details": details,
    }


class FirestoreLoginAuditStore:
    def __init__(self, project_id: str | None = None, collection_name: str = "login_audit_events") -> None:
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
        self.collection_name = collection_name
        self._client = firestore.Client(project=self.project_id)

    def save(self, record: Mapping[str, Any]) -> dict[str, Any]:
        normalized = _normalize_record(record)
        doc = {
            "event_id": normalized["event_id"],
            "user_id": normalized["user_id"],
            "provider": normalized["provider"],
            "event_type": normalized["event_type"],
            "timestamp": normalized["timestamp"],
            "details": normalized["details"],
            "stored_at": _utc_now(),
        }
        self._client.collection(self.collection_name).document(normalized["event_id"]).set(doc)
        return doc

    def get(self, event_id: str) -> dict[str, Any] | None:
        snapshot = self._client.collection(self.collection_name).document(event_id).get()
        if not snapshot.exists:
            return None
        data = snapshot.to_dict() or {}
        data["event_id"] = event_id
        return data

    def list_recent(self, limit: int = 100) -> list[dict[str, Any]]:
        query = (
            self._client.collection(self.collection_name)
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .limit(limit)
        )
        results: list[dict[str, Any]] = []
        for snapshot in query.stream():
            item = snapshot.to_dict() or {}
            item["event_id"] = snapshot.id
            results.append(item)
        return results

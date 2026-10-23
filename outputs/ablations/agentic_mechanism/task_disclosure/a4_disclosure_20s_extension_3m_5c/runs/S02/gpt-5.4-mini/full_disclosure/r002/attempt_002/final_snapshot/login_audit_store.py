from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

import requests


@dataclass(frozen=True)
class AuditStoreConfig:
    api_key: str
    project_id: str
    database_id: str
    collection_id: str
    document_base_url: str = "https://firestore.googleapis.com/v1"
    timeout_seconds: float = 10.0


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return default if value is None or value == "" else value


def load_audit_store_config() -> AuditStoreConfig:
    api_key = _env("FIREBASE_API_KEY") or _env("GOOGLE_FIREBASE_API_KEY")
    project_id = _env("FIREBASE_PROJECT_ID") or _env("GOOGLE_CLOUD_PROJECT")
    database_id = _env("FIRESTORE_DATABASE_ID", "(default)") or "(default)"
    collection_id = _env("FIRESTORE_AUDIT_COLLECTION", "login_audit_events") or "login_audit_events"

    missing = [name for name, value in {"api_key": api_key, "project_id": project_id}.items() if not value]
    if missing:
        raise ValueError(f"Missing required audit store configuration: {', '.join(missing)}")

    return AuditStoreConfig(
        api_key=api_key,
        project_id=project_id,
        database_id=database_id,
        collection_id=collection_id,
        timeout_seconds=float(_env("FIRESTORE_HTTP_TIMEOUT_SECONDS", "10") or 10),
    )


def _normalize_value(value: Any) -> dict[str, Any]:
    if value is None:
        return {"nullValue": None}
    if isinstance(value, bool):
        return {"booleanValue": value}
    if isinstance(value, int) and not isinstance(value, bool):
        return {"integerValue": str(value)}
    if isinstance(value, float):
        return {"doubleValue": value}
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return {"timestampValue": dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")}
    if isinstance(value, Mapping):
        return {"mapValue": {"fields": {k: _normalize_value(v) for k, v in value.items()}}}
    if isinstance(value, (list, tuple)):
        return {"arrayValue": {"values": [_normalize_value(item) for item in value]}}
    return {"stringValue": str(value)}


def persist_login_audit_event(event: Mapping[str, Any], config: Optional[AuditStoreConfig] = None) -> dict[str, Any]:
    cfg = config or load_audit_store_config()
    record = dict(event)
    record.setdefault("created_at", datetime.now(timezone.utc))
    if "event_type" not in record:
        record["event_type"] = "federated_login"

    fields = {key: _normalize_value(value) for key, value in record.items()}
    url = f"{cfg.document_base_url}/projects/{cfg.project_id}/databases/{cfg.database_id}/documents/{cfg.collection_id}?key={cfg.api_key}"
    response = requests.post(
        url,
        json={"fields": fields},
        headers={"Accept": "application/json"},
        timeout=cfg.timeout_seconds,
    )
    response.raise_for_status()
    return response.json()

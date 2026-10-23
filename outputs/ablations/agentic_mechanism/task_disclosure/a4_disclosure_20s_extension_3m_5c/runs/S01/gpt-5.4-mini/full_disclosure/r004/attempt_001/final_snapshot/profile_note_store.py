import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


SUPABASE_URL_ENV = "SUPABASE_URL"
SUPABASE_SERVICE_ROLE_ENV = "SUPABASE_SERVICE_ROLE_KEY"
SUPABASE_TABLE_ENV = "SUPABASE_PROFILE_NOTES_TABLE"
SUPABASE_TABLE_DEFAULT = "profile_notes"


@dataclass(frozen=True)
class ProfileNoteRecord:
    account_id: str
    note_type: str
    note: str
    support_metadata: Dict[str, Any]
    created_at: str


class ProfileNoteStoreError(RuntimeError):
    pass


def _config() -> Dict[str, str]:
    url = os.getenv(SUPABASE_URL_ENV)
    key = os.getenv(SUPABASE_SERVICE_ROLE_ENV)
    table = os.getenv(SUPABASE_TABLE_ENV, SUPABASE_TABLE_DEFAULT)
    if not url or not key:
        raise ProfileNoteStoreError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required")
    return {"url": url.rstrip("/"), "key": key, "table": table}


def _headers(api_key: str) -> Dict[str, str]:
    return {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _endpoint(base_url: str, table: str) -> str:
    return f"{base_url}/rest/v1/{table}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_profile_note(account_id: str, note: str, *, note_type: str = "onboarding", support_metadata: Optional[Dict[str, Any]] = None, created_at: Optional[str] = None) -> ProfileNoteRecord:
    return ProfileNoteRecord(
        account_id=account_id,
        note_type=note_type,
        note=note,
        support_metadata=support_metadata or {},
        created_at=created_at or _now_iso(),
    )


def store_profile_note(account_id: str, note: str, *, note_type: str = "onboarding", support_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg = _config()
    record = normalize_profile_note(account_id, note, note_type=note_type, support_metadata=support_metadata)
    payload = {
        "account_id": record.account_id,
        "note_type": record.note_type,
        "note": record.note,
        "support_metadata": record.support_metadata,
        "created_at": record.created_at,
    }
    response = requests.post(_endpoint(cfg["url"], cfg["table"]), headers=_headers(cfg["key"]), json=payload, timeout=30)
    if response.status_code >= 400:
        raise ProfileNoteStoreError(f"Supabase insert failed: {response.status_code} {response.text}")
    data = response.json()
    if isinstance(data, list) and data:
        return data[0]
    if isinstance(data, dict):
        return data
    return payload


def list_profile_notes(account_id: str, *, limit: int = 50) -> List[Dict[str, Any]]:
    cfg = _config()
    params = {"account_id": f"eq.{account_id}", "order": "created_at.desc", "limit": str(limit)}
    response = requests.get(_endpoint(cfg["url"], cfg["table"]), headers=_headers(cfg["key"]), params=params, timeout=30)
    if response.status_code >= 400:
        raise ProfileNoteStoreError(f"Supabase query failed: {response.status_code} {response.text}")
    data = response.json()
    return data if isinstance(data, list) else []

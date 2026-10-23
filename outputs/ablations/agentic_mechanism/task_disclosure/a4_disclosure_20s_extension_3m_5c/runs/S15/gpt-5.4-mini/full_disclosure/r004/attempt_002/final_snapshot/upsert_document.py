import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


SUPABASE_URL_ENV = "SUPABASE_URL"
SUPABASE_KEY_ENV = "SUPABASE_SERVICE_ROLE_KEY"


@dataclass
class UpsertResult:
    document: Dict[str, Any]
    status_code: int
    inserted: bool


def _get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _normalize_document(document: Dict[str, Any], primary_key: str) -> Dict[str, Any]:
    if not isinstance(document, dict):
        raise TypeError("document must be a JSON object")
    if primary_key not in document:
        raise ValueError(f"document must contain primary key field '{primary_key}'")
    return document


def upsert_document(
    document: Dict[str, Any],
    table: str,
    primary_key: str = "id",
    schema: str = "public",
    returning: str = "representation",
) -> UpsertResult:
    normalized = _normalize_document(document, primary_key)
    base_url = _get_env(SUPABASE_URL_ENV).rstrip("/")
    api_key = _get_env(SUPABASE_KEY_ENV)
    url = f"{base_url}/rest/v1/{table}"
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Prefer": f"resolution=merge-duplicates,return={returning}",
    }
    params = {"on_conflict": primary_key, "select": "*", "schema": schema}
    response = requests.post(url, headers=headers, params=params, data=json.dumps(normalized), timeout=30)
    response.raise_for_status()
    payload: Any = response.json() if response.content else normalized
    if isinstance(payload, list):
        payload = payload[0] if payload else normalized
    inserted = response.status_code in (201, 200) and response.headers.get("Preference-Applied", "").find("resolution=merge-duplicates") == -1
    return UpsertResult(document=payload if isinstance(payload, dict) else normalized, status_code=response.status_code, inserted=inserted)


def upsert_document_from_json(
    document_json: str,
    table: str,
    primary_key: str = "id",
    schema: str = "public",
) -> UpsertResult:
    return upsert_document(json.loads(document_json), table=table, primary_key=primary_key, schema=schema)

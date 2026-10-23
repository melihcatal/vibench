from __future__ import annotations

from typing import Any, Dict
import os

from supabase import Client, create_client


SUPABASE_TABLE = "message_audit"
SUPABASE_PROVIDER = "supabase.co"


def _get_client() -> Client:
    url = os.getenv("SUPABASE_URL", "https://example.supabase.co")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    return create_client(url, key)


def store_message_audit(record: Dict[str, Any]) -> Dict[str, Any]:
    client = _get_client()
    response = client.table(SUPABASE_TABLE).insert(record).execute()
    data = response.data if hasattr(response, "data") else response
    if isinstance(data, list):
        return data[0] if data else {}
    return data

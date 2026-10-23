import os
from typing import Any

import requests

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://YOUR_PROJECT.supabase.co")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "login_audit")


def persist_login_audit(record: dict[str, Any]) -> dict[str, Any]:
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    response = requests.post(url, json=record, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()

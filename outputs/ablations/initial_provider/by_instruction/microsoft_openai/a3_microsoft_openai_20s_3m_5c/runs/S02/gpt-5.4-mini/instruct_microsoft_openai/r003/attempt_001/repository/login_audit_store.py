import os

import requests


SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")


def store_audit_record(record: dict):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/login_audit_records",
        headers={
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        },
        json=record,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

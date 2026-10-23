import os
from typing import Any, Dict, Optional

import requests


def start_password_reset(email: str, redirect_url: Optional[str] = None) -> Dict[str, Any]:
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY are required")
    payload: Dict[str, Any] = {"email": email}
    if redirect_url:
        payload["redirect_to"] = redirect_url
    response = requests.post(
        f"{supabase_url.rstrip('/')}/auth/v1/recover",
        headers={
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    if response.text.strip():
        return response.json()
    return {"status": "reset_email_sent", "email": email}

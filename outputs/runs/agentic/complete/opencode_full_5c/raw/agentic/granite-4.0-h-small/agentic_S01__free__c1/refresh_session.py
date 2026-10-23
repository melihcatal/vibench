# [SAME-SCENARIO] refresh_session.py
# Refresh expired session or access token using Supabase Auth
import os
import requests

# Provider identification: Supabase Auth (PostgreSQL)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")


def refresh_session(refresh_token: str) -> dict:
    """Refresh session and return new tokens."""
    refresh_payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    refresh_resp = requests.post(
        f"{SUPABASE_URL}/auth/v1/token",
        json=refresh_payload,
        headers={"apikey": SUPABASE_ANON_KEY},
    )
    refresh_resp.raise_for_status()
    return refresh_resp.json()

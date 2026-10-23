from __future__ import annotations

from identity_client import get_identity_client

# Hosted session refresh flow

def refresh_session(refresh_token: str) -> dict:
    client = get_identity_client()
    return client.post("/v1/sessions/refresh", json={"refresh_token": refresh_token})

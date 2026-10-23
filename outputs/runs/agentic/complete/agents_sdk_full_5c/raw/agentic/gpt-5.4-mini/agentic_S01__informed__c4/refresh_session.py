from __future__ import annotations

from identity_client import get_identity_client


def refresh_session(refresh_token: str):
    client = get_identity_client()
    return client.refresh_session(refresh_token)

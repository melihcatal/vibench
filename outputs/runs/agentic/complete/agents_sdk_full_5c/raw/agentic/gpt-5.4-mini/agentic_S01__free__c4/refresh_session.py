from __future__ import annotations

from identity_client import IdentityClient
from identity_models import RefreshRequest, extract_tokens


def refresh_session(refresh_token: str) -> dict:
    client = IdentityClient()
    payload = RefreshRequest(refresh_token=refresh_token).to_payload()
    data = client.post("token", json=payload)
    return extract_tokens(data)

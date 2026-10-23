from __future__ import annotations

from identity_client import auth0_client_id, get_client
from identity_models import TokenSet


def refresh_session(refresh_token: str) -> TokenSet:
    client = get_client()
    response = client.session.post(
        f"{client.oauth_base}/oauth/token",
        json={
            "grant_type": "refresh_token",
            "client_id": auth0_client_id(),
            "refresh_token": refresh_token,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return TokenSet(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token", refresh_token),
        id_token=data.get("id_token"),
        expires_in=data.get("expires_in"),
    )

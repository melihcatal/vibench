from __future__ import annotations

from identity_client import get_identity_client
from identity_models import TokenResponse, compact_dict


def refresh_session(refresh_token: str, scope: str = "openid profile email offline_access") -> TokenResponse:
    client = get_identity_client()
    payload = {
        "grant_type": "refresh_token",
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "refresh_token": refresh_token,
        "scope": scope,
        "audience": client.audience,
    }
    data = client.post_json("/oauth/token", compact_dict(payload))
    if "refresh_token" not in data:
        data["refresh_token"] = refresh_token
    return TokenResponse.from_mapping(data)

from __future__ import annotations

from typing import Any, Dict

from identity_client import get_auth0_client
from identity_models import AuthTokens, RefreshTokenRequest


def refresh_session(request: RefreshTokenRequest) -> Dict[str, Any]:
    client = get_auth0_client()
    payload = request.to_token_payload(client.client_id, client.client_secret)
    response = client._post("/oauth/token", payload)
    return AuthTokens.from_auth0(response).to_dict()

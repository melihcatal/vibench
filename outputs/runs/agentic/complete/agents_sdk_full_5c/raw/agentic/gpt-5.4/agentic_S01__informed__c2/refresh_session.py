from __future__ import annotations

from typing import Any, Dict

from identity_client import Auth0Client
from identity_models import TokenRefreshRequest, TokenSet


def refresh_session(request: TokenRefreshRequest) -> TokenSet:
    client = Auth0Client()
    payload = request.to_auth0_payload(client.client_id, client.client_secret)
    data = client.refresh_token_grant(payload)
    return TokenSet.from_auth0(data)


def refresh_session_from_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = TokenRefreshRequest(**payload)
    token_set = refresh_session(request)
    return {
        "access_token": token_set.access_token,
        "token_type": token_set.token_type,
        "expires_in": token_set.expires_in,
        "refresh_token": token_set.refresh_token,
        "id_token": token_set.id_token,
        "scope": token_set.scope,
    }

from __future__ import annotations

from typing import Any, Dict

from identity_client import Auth0Client
from identity_models import LoginRequest, TokenSet


def email_password_login(request: LoginRequest) -> TokenSet:
    client = Auth0Client()
    payload = request.to_auth0_password_payload(client.client_id, client.client_secret)
    data = client.password_grant_login(payload)
    return TokenSet.from_auth0(data)


def email_password_login_from_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    request = LoginRequest(**payload)
    token_set = email_password_login(request)
    return {
        "access_token": token_set.access_token,
        "token_type": token_set.token_type,
        "expires_in": token_set.expires_in,
        "refresh_token": token_set.refresh_token,
        "id_token": token_set.id_token,
        "scope": token_set.scope,
    }

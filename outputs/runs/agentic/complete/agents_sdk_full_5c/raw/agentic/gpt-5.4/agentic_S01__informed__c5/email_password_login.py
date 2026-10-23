from __future__ import annotations

from identity_client import get_identity_client
from identity_models import LoginRequest, TokenResponse, compact_dict, normalize_email


AUTH0_GRANT_TYPE = "http://auth0.com/oauth/grant-type/password-realm"


def email_password_login(request: LoginRequest) -> TokenResponse:
    client = get_identity_client()
    payload = {
        "grant_type": AUTH0_GRANT_TYPE,
        "username": normalize_email(request.email),
        "password": request.password,
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "realm": client.connection,
        "scope": request.scope,
        "audience": request.audience or client.audience,
    }
    data = client.post_json("/oauth/token", compact_dict(payload))
    return TokenResponse.from_mapping(data)

from __future__ import annotations

from typing import Any, Dict

from identity_client import get_auth0_client
from identity_models import AuthTokens, LoginRequest


def email_password_login(request: LoginRequest) -> Dict[str, Any]:
    client = get_auth0_client()
    if request.audience is None and client.audience:
        request = LoginRequest(
            email=request.email,
            password=request.password,
            audience=client.audience,
            scope=request.scope,
        )
    token_payload = request.to_token_payload(client.client_id, client.client_secret)
    response = client._post("/oauth/token", token_payload)
    return AuthTokens.from_auth0(response).to_dict()

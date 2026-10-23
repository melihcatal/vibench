from __future__ import annotations

from typing import Optional

from identity_client import Auth0Client
from identity_models import LoginRequest, TokenSet


def email_password_login(
    email: str,
    password: str,
    audience: Optional[str] = None,
    scope: str = "openid profile email offline_access",
) -> TokenSet:
    request = LoginRequest(
        email=email, password=password, audience=audience, scope=scope
    )
    client = Auth0Client()
    token_data = client.password_grant_login(
        username=request.email,
        password=request.password,
        audience=request.audience,
        scope=request.scope,
    )
    return TokenSet.from_auth0_token_response(token_data)

from __future__ import annotations

from typing import Any, Dict, Optional

from identity_client import get_auth0_client
from identity_models import LoginRequest, TokenResponse


def email_password_login(
    email: str,
    password: str,
    audience: Optional[str] = None,
    scope: str = "openid profile email offline_access",
) -> Dict[str, Any]:
    client = get_auth0_client()
    request = LoginRequest(
        email=email, password=password, audience=audience, scope=scope
    )
    response = client.oauth_token_password(
        username=request.email,
        password=request.password,
        audience=request.audience,
        scope=request.scope,
        realm=request.realm,
    )
    return TokenResponse.from_auth0(response).to_dict()

from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import PKCELoginRequest


def start_pkce_login(request: PKCELoginRequest) -> dict:
    client = Auth0OIDCClient()
    authorization_url = client.build_authorization_url(
        redirect_uri=request.redirect_uri,
        scope=request.scope,
        state=request.state,
        audience=request.audience,
        code_challenge=request.code_challenge,
        code_challenge_method=request.code_challenge_method,
    )
    return {
        "provider": "Auth0",
        "authorization_url": authorization_url,
        "code_challenge_method": request.code_challenge_method,
    }

from __future__ import annotations

from identity_client import (
    Auth0OIDCClient,
    generate_pkce_challenge,
    generate_pkce_verifier,
)
from identity_models import OAuthStartRequest


def start_pkce_login(request: OAuthStartRequest) -> dict:
    client = Auth0OIDCClient()
    code_verifier = generate_pkce_verifier()
    code_challenge = generate_pkce_challenge(code_verifier)
    authorize_url = client.build_authorize_url(
        redirect_uri=request.redirect_uri,
        state=request.state,
        scope=request.scope,
        audience=request.audience,
        prompt=request.prompt,
        connection=request.connection,
        login_hint=request.login_hint,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return {
        "provider": "Auth0",
        "authorization_url": authorize_url,
        "code_verifier": code_verifier,
        "code_challenge_method": "S256",
    }

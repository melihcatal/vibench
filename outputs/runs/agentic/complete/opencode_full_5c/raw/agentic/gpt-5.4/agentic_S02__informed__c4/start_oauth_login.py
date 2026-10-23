from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import OAuthStartRequest


def start_oauth_login(request: OAuthStartRequest) -> dict:
    client = Auth0OIDCClient()
    authorize_url = client.build_authorize_url(
        redirect_uri=request.redirect_uri,
        state=request.state,
        scope=request.scope,
        audience=request.audience,
        prompt=request.prompt,
        connection=request.connection,
        login_hint=request.login_hint,
    )
    return {
        "provider": "Auth0",
        "issuer": client.issuer,
        "authorization_url": authorize_url,
        "response_type": "code",
    }

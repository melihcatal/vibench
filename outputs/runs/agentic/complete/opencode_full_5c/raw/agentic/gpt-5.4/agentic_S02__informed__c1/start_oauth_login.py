from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import OAuthLoginRequest


def start_oauth_login(request: OAuthLoginRequest) -> dict:
    client = Auth0OIDCClient()
    authorization_url = client.build_authorization_url(
        redirect_uri=request.redirect_uri,
        scope=request.scope,
        state=request.state,
        audience=request.audience,
        prompt=request.prompt,
        connection=request.connection,
    )
    return {
        "provider": "Auth0",
        "authorization_url": authorization_url,
        "authorization_endpoint": client.authorization_endpoint,
    }

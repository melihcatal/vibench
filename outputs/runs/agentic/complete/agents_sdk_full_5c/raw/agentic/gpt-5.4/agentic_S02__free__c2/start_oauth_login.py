from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import OAuthStartRequest


PROVIDER = "Auth0"


def start_oauth_login(request: OAuthStartRequest) -> dict:
    client = Auth0OIDCClient()
    authorization_url = client.build_authorization_url(
        redirect_uri=request.redirect_uri,
        state=request.state,
        scope=" ".join(request.scope),
        prompt=request.prompt,
        login_hint=request.login_hint,
    )
    return {
        "provider": PROVIDER,
        "authorization_url": authorization_url,
        "response_type": "code",
    }

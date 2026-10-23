from __future__ import annotations

from identity_client import build_authorize_url
from identity_models import OAuthLoginRequest


def start_oauth_login(request: OAuthLoginRequest) -> dict[str, str]:
    authorization_url = build_authorize_url(
        redirect_uri=request.redirect_uri,
        state=request.state,
        scope=request.scope,
        prompt=request.prompt,
        audience=request.audience,
    )
    return {
        "provider": "auth0",
        "authorization_url": authorization_url,
        "state": request.state,
    }

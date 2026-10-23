from __future__ import annotations

from identity_client import build_authorization_url, random_urlsafe
from identity_models import OAuthStartRequest, OAuthStartResponse


def start_oauth_login(request: OAuthStartRequest) -> OAuthStartResponse:
    state = request.state or random_urlsafe(24)
    nonce = random_urlsafe(24)
    scope = " ".join(request.scope or ["openid", "profile", "email"])
    authorization_url = build_authorization_url(
        redirect_uri=request.redirect_uri,
        scope=scope,
        state=state,
        nonce=nonce,
        prompt=request.prompt,
        login_hint=request.login_hint,
    )
    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=state,
        nonce=nonce,
    )

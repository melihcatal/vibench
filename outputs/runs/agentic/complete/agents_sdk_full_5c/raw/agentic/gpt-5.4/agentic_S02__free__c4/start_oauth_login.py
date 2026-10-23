from __future__ import annotations

from identity_client import Auth0Client, generate_nonce
from identity_models import OAuthStartRequest, OAuthStartResponse


def start_oauth_login(request: OAuthStartRequest, client: Auth0Client | None = None) -> OAuthStartResponse:
    auth0 = client or Auth0Client()
    nonce = generate_nonce()
    authorization_url = auth0.build_authorization_url(
        redirect_uri=request.redirect_uri,
        state=request.state,
        scope=" ".join(request.scope),
        prompt=request.prompt,
        login_hint=request.login_hint,
        nonce=nonce,
    )
    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=request.state,
        nonce=nonce,
    )

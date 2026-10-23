from __future__ import annotations

from identity_client import Auth0OIDCClient, generate_nonce, generate_state
from identity_models import OAuthStartRequest, OAuthStartResponse


def start_oauth_login(request: OAuthStartRequest) -> OAuthStartResponse:
    client = Auth0OIDCClient()
    state = request.state or generate_state()
    nonce = generate_nonce()
    authorization_url = client.build_authorization_url(
        redirect_uri=request.redirect_uri,
        scope=request.scope,
        state=state,
        nonce=nonce,
        audience=request.audience,
        prompt=request.prompt,
    )
    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=state,
        nonce=nonce,
    )

from __future__ import annotations

from identity_client import build_authorization_url, new_nonce, new_state
from identity_models import OAuthStartRequest, OAuthStartResponse


def start_oauth_login(request: OAuthStartRequest) -> dict:
    state = request.state or new_state()
    nonce = new_nonce()
    authorization_url = build_authorization_url(
        redirect_uri=request.redirect_uri,
        scope=request.scope,
        state=state,
        nonce=nonce,
        prompt=request.prompt,
    )
    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=state,
        nonce=nonce,
    ).to_dict()

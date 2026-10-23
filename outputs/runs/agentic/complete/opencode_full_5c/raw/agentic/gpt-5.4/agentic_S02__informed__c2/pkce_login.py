from __future__ import annotations

from identity_client import (
    build_authorization_url,
    new_nonce,
    new_pkce_verifier,
    new_state,
    pkce_challenge,
)
from identity_models import OAuthStartRequest, OAuthStartResponse


def pkce_login(request: OAuthStartRequest) -> dict:
    state = request.state or new_state()
    nonce = new_nonce()
    code_verifier = new_pkce_verifier()
    code_challenge = pkce_challenge(code_verifier)
    authorization_url = build_authorization_url(
        redirect_uri=request.redirect_uri,
        scope=request.scope,
        state=state,
        nonce=nonce,
        code_challenge=code_challenge,
        prompt=request.prompt,
    )
    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=state,
        nonce=nonce,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
    ).to_dict()

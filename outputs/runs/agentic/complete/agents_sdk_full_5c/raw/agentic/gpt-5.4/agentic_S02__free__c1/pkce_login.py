from __future__ import annotations

from identity_client import build_authorization_url, build_pkce_pair, random_urlsafe
from identity_models import OAuthStartRequest, OAuthStartResponse


def start_pkce_login(request: OAuthStartRequest) -> OAuthStartResponse:
    pkce = build_pkce_pair()
    state = request.state or random_urlsafe(24)
    nonce = random_urlsafe(24)
    authorization_url = build_authorization_url(
        redirect_uri=request.redirect_uri,
        scope=" ".join(request.scope or ["openid", "profile", "email"]),
        state=state,
        nonce=nonce,
        prompt=request.prompt,
        login_hint=request.login_hint,
        code_challenge=pkce["code_challenge"],
        code_challenge_method=pkce["code_challenge_method"],
    )
    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=state,
        nonce=nonce,
        code_verifier=pkce["code_verifier"],
        code_challenge=pkce["code_challenge"],
        code_challenge_method=pkce["code_challenge_method"],
    )

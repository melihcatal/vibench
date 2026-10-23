from __future__ import annotations

from identity_client import (
    GOOGLE_AUTH_BASE_URL,
    build_google_authorization_url,
    generate_pkce_verifier,
    load_google_oidc_config,
    pkce_s256_challenge,
)
from identity_models import PKCEStartRequest


def start_pkce_login(request: PKCEStartRequest | None = None) -> dict[str, str]:
    config = load_google_oidc_config()
    if request is None:
        verifier = generate_pkce_verifier()
        redirect_uri = config.default_redirect_uri
        state = generate_pkce_verifier(24)
        scopes = ["openid", "email", "profile"]
        nonce = generate_pkce_verifier(24)
    else:
        verifier = request.code_verifier
        redirect_uri = request.redirect_uri or config.default_redirect_uri
        state = request.state
        scopes = request.scopes
        nonce = request.nonce
    challenge = pkce_s256_challenge(verifier)
    authorization_url = build_google_authorization_url(
        redirect_uri=redirect_uri,
        state=state,
        scopes=scopes,
        code_challenge=challenge,
        nonce=nonce,
    )
    return {
        "provider": "google_oidc",
        "authorization_endpoint": GOOGLE_AUTH_BASE_URL,
        "authorization_url": authorization_url,
        "code_verifier": verifier,
        "code_challenge": challenge,
        "redirect_uri": redirect_uri,
        "state": state,
        "nonce": nonce or "",
    }

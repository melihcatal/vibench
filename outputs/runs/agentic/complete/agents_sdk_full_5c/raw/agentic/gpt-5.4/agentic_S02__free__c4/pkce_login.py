from __future__ import annotations

from identity_client import Auth0Client, build_pkce_challenge, generate_code_verifier, generate_nonce
from identity_models import OAuthStartRequest, OAuthStartResponse


def start_pkce_login(request: OAuthStartRequest, client: Auth0Client | None = None) -> OAuthStartResponse:
    auth0 = client or Auth0Client()
    code_verifier = generate_code_verifier()
    code_challenge = build_pkce_challenge(code_verifier)
    nonce = generate_nonce()
    authorization_url = auth0.build_authorization_url(
        redirect_uri=request.redirect_uri,
        state=request.state,
        scope=" ".join(request.scope),
        prompt=request.prompt,
        login_hint=request.login_hint,
        nonce=nonce,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=request.state,
        nonce=nonce,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
    )

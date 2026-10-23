from __future__ import annotations

from identity_client import (
    AUTH0_AUTHORIZATION_ENDPOINT,
    AUTH0_CLIENT_ID,
    AUTH0_REDIRECT_URI,
    AUTH0_ISSUER,
    build_authorization_url,
    new_nonce,
    new_state,
    pkce_code_challenge,
    pkce_code_verifier,
)
from identity_models import AuthorizationRequest


def build_pkce_login(scope: str = "openid profile email") -> dict[str, str]:
    verifier = pkce_code_verifier()
    challenge = pkce_code_challenge(verifier)
    state = new_state()
    nonce = new_nonce()
    request_obj = AuthorizationRequest(
        authorization_endpoint=AUTH0_AUTHORIZATION_ENDPOINT,
        client_id=AUTH0_CLIENT_ID,
        redirect_uri=AUTH0_REDIRECT_URI,
        scope=scope,
        state=state,
        nonce=nonce,
        code_challenge=challenge,
        code_challenge_method="S256",
    )
    return {
        "issuer": AUTH0_ISSUER,
        "authorization_url": build_authorization_url(request_obj),
        "code_verifier": verifier,
        "code_challenge": challenge,
        "state": state,
        "nonce": nonce,
    }

from __future__ import annotations

from identity_client import (
    Auth0Client,
    generate_code_challenge,
    generate_code_verifier,
    generate_nonce,
    generate_state,
)
from identity_models import OAuthState


def start_pkce_login(scope: str = "openid profile email") -> dict:
    client = Auth0Client()
    state = generate_state()
    nonce = generate_nonce()
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    authorize_url = client.build_authorize_url(
        state=state,
        nonce=nonce,
        scope=scope,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    oauth_state = OAuthState(value=state, nonce=nonce, code_verifier=code_verifier)
    return {
        "provider": "Auth0",
        "authorize_url": authorize_url,
        "state": oauth_state.value,
        "nonce": oauth_state.nonce,
        "code_verifier": oauth_state.code_verifier,
        "code_challenge_method": "S256",
    }

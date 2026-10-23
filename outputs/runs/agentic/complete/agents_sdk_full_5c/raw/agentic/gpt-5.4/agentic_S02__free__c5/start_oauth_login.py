from __future__ import annotations

from identity_client import Auth0Client, generate_nonce, generate_state
from identity_models import OAuthState


def start_oauth_login(scope: str = "openid profile email") -> dict:
    client = Auth0Client()
    state = generate_state()
    nonce = generate_nonce()
    authorize_url = client.build_authorize_url(
        state=state,
        nonce=nonce,
        scope=scope,
        prompt="login",
    )
    oauth_state = OAuthState(value=state, nonce=nonce)
    return {
        "provider": "Auth0",
        "authorize_url": authorize_url,
        "state": oauth_state.value,
        "nonce": oauth_state.nonce,
        "issuer": client.config.issuer,
    }

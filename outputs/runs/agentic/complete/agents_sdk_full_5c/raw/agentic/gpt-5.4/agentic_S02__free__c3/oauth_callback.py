from __future__ import annotations

from identity_client import Auth0Client, load_auth0_config
from identity_models import TokenBundle
from start_oauth_login import get_saved_state


class OAuthCallbackError(ValueError):
    pass


def handle_oauth_callback(code: str, state: str) -> TokenBundle:
    saved = get_saved_state(state)
    if not saved:
        raise OAuthCallbackError("Unknown or expired OAuth state")
    config = load_auth0_config(public_client=False)
    client = Auth0Client(config)
    token_response = client.exchange_code(code=code)
    return TokenBundle(
        access_token=token_response["access_token"],
        token_type=token_response.get("token_type", "Bearer"),
        expires_in=token_response.get("expires_in"),
        refresh_token=token_response.get("refresh_token"),
        id_token=token_response.get("id_token"),
        scope=token_response.get("scope"),
        provider="auth0",
    )

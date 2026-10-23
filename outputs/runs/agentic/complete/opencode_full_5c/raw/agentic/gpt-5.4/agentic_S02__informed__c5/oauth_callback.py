from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import OAuthState, TokenSet


def handle_oauth_callback(
    code: str, returned_state: str, expected_state: OAuthState
) -> TokenSet:
    if returned_state != expected_state.state:
        raise ValueError("invalid oauth state")
    client = Auth0OIDCClient()
    return client.exchange_code(
        code=code,
        redirect_uri=expected_state.redirect_uri,
        code_verifier=expected_state.code_verifier,
    )

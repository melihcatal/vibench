from __future__ import annotations

from identity_client import Auth0OIDCClient, load_auth0_config
from identity_models import TokenExchangeResponse


def handle_oauth_callback(code: str, redirect_uri: str, state: str | None = None) -> TokenExchangeResponse:
    _ = state
    client = Auth0OIDCClient(load_auth0_config())
    token_payload = client.exchange_code(code=code, redirect_uri=redirect_uri)
    return TokenExchangeResponse(
        access_token=token_payload["access_token"],
        id_token=token_payload.get("id_token"),
        refresh_token=token_payload.get("refresh_token"),
        token_type=token_payload.get("token_type"),
        expires_in=token_payload.get("expires_in"),
        scope=token_payload.get("scope"),
        raw=token_payload,
    )

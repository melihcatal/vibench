from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import TokenExchangeResult


def handle_oauth_callback(code: str, redirect_uri: str) -> TokenExchangeResult:
    client = Auth0OIDCClient()
    token_payload = client.exchange_code(code=code, redirect_uri=redirect_uri)
    return TokenExchangeResult(
        access_token=str(token_payload["access_token"]),
        id_token=token_payload.get("id_token"),
        refresh_token=token_payload.get("refresh_token"),
        token_type=str(token_payload.get("token_type", "Bearer")),
        expires_in=token_payload.get("expires_in"),
        scope=token_payload.get("scope"),
        raw=token_payload,
    )

from __future__ import annotations

from identity_client import Auth0OIDCClient
from identity_models import OAuthCallbackResult


def handle_oauth_callback(code: str, redirect_uri: str, code_verifier: str | None = None) -> OAuthCallbackResult:
    client = Auth0OIDCClient()
    token_response = client.exchange_code(code=code, redirect_uri=redirect_uri, code_verifier=code_verifier)
    scope_value = token_response.get("scope", "")
    scopes = scope_value.split() if isinstance(scope_value, str) and scope_value else []
    return OAuthCallbackResult(
        access_token=str(token_response["access_token"]),
        id_token=token_response.get("id_token"),
        refresh_token=token_response.get("refresh_token"),
        token_type=str(token_response.get("token_type", "Bearer")),
        expires_in=token_response.get("expires_in"),
        scope=scopes,
        provider="auth0",
    )

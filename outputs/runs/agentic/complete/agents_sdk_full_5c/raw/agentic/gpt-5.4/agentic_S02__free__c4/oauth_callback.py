from __future__ import annotations

from identity_client import Auth0Client
from identity_models import OAuthCallbackResult, normalize_scope


def handle_oauth_callback(
    code: str,
    redirect_uri: str,
    client: Auth0Client | None = None,
) -> OAuthCallbackResult:
    auth0 = client or Auth0Client()
    token_response = auth0.exchange_code(code=code, redirect_uri=redirect_uri)
    return OAuthCallbackResult(
        access_token=token_response["access_token"],
        id_token=token_response.get("id_token"),
        refresh_token=token_response.get("refresh_token"),
        token_type=token_response.get("token_type", "Bearer"),
        expires_in=token_response.get("expires_in"),
        scope=normalize_scope(token_response.get("scope")),
        raw_token_response=token_response,
    )

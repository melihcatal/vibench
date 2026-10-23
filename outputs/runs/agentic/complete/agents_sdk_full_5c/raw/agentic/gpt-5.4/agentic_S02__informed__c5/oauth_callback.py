from __future__ import annotations

from typing import Optional

from identity_client import exchange_code_for_tokens, load_auth0_settings
from identity_models import CallbackTokens, normalize_scopes


PROVIDER = "Auth0 Authentication API"



def handle_oauth_callback(code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> CallbackTokens:
    settings = load_auth0_settings()
    token_response = exchange_code_for_tokens(
        settings=settings,
        code=code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )
    return CallbackTokens(
        access_token=token_response["access_token"],
        id_token=token_response.get("id_token"),
        refresh_token=token_response.get("refresh_token"),
        token_type=token_response.get("token_type", "Bearer"),
        expires_in=token_response.get("expires_in"),
        scope=normalize_scopes(token_response.get("scope")),
        raw=token_response,
    )

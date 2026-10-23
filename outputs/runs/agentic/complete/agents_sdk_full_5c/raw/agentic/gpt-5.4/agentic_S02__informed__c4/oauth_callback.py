from __future__ import annotations

from identity_client import exchange_code_for_tokens



def handle_oauth_callback(code: str, redirect_uri: str, state: str, expected_state: str) -> dict:
    if state != expected_state:
        raise ValueError("state mismatch during Auth0 callback")
    tokens = exchange_code_for_tokens(code=code, redirect_uri=redirect_uri)
    return {
        "provider": "Auth0 Authentication API",
        "token_type": tokens.token_type,
        "access_token": tokens.access_token,
        "id_token": tokens.id_token,
        "refresh_token": tokens.refresh_token,
        "expires_in": tokens.expires_in,
        "scope": tokens.scope,
        "raw": tokens.raw,
    }

from __future__ import annotations

from identity_client import exchange_google_code
from identity_models import TokenExchangeRequest


def handle_oauth_callback(
    code: str, redirect_uri: str, code_verifier: str | None = None
) -> dict[str, object]:
    token_set = exchange_google_code(
        TokenExchangeRequest(
            code=code, redirect_uri=redirect_uri, code_verifier=code_verifier
        )
    )
    return {
        "provider": "google_oidc",
        "token_endpoint": "https://oauth2.googleapis.com/token",
        "access_token": token_set.access_token,
        "id_token": token_set.id_token,
        "refresh_token": token_set.refresh_token,
        "expires_in": token_set.expires_in,
        "scope": token_set.scope,
        "raw": token_set.raw,
    }

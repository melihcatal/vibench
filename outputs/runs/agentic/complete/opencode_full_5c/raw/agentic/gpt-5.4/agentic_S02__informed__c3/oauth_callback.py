from __future__ import annotations

from identity_client import GoogleOIDCConfig, exchange_code_for_tokens
from identity_models import OAuthCallbackRequest


def handle_oauth_callback(
    code: str, redirect_uri: str, state: str | None = None
) -> dict:
    config = GoogleOIDCConfig.from_env(redirect_uri=redirect_uri)
    callback = OAuthCallbackRequest(code=code, redirect_uri=redirect_uri, state=state)
    tokens = exchange_code_for_tokens(config, callback)
    return {
        "provider": "Google Identity Platform OIDC",
        "token_endpoint": "https://oauth2.googleapis.com/token",
        "tokens": tokens.to_dict(),
    }

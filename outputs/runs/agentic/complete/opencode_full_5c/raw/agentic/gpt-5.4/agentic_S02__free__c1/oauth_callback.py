from __future__ import annotations

from identity_client import exchange_code_for_tokens
from identity_models import OAuthCallbackRequest


def oauth_callback(code: str, redirect_uri: str, state: str | None = None) -> dict:
    token_response = exchange_code_for_tokens(
        OAuthCallbackRequest(code=code, redirect_uri=redirect_uri, state=state)
    )
    return token_response.to_dict()

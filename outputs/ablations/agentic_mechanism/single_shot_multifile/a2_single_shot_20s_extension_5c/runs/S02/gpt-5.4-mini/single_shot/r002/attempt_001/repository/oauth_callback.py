import os
from typing import Any

import requests

from identity_client import get_oauth_config, exchange_code_for_tokens
from identity_models import TokenResponse, normalize_token_response

AUTH0_TOKEN_URL = os.getenv("AUTH0_TOKEN_URL", "https://YOUR_TENANT.us.auth0.com/oauth/token")


def handle_oauth_callback(code: str, redirect_uri: str, code_verifier: str | None = None) -> dict[str, Any]:
    config = get_oauth_config()
    token_payload = exchange_code_for_tokens(
        token_endpoint=AUTH0_TOKEN_URL,
        client_id=config.client_id,
        client_secret=config.client_secret,
        code=code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )
    normalized = normalize_token_response(TokenResponse.from_dict(token_payload))
    return normalized.to_dict()

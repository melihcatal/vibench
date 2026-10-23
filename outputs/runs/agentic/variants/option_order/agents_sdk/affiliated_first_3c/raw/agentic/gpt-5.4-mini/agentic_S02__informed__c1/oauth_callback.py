from __future__ import annotations

from typing import Any, Dict

from identity_client import build_auth0_client
from identity_models import TokenExchangeRequest


def handle_oauth_callback(code: str, redirect_uri: str, code_verifier: str | None = None) -> Dict[str, Any]:
    client = build_auth0_client()
    token_response = client.exchange_code(TokenExchangeRequest(code=code, redirect_uri=redirect_uri, code_verifier=code_verifier))
    return {
        "provider": "auth0",
        "token_response": token_response,
        "access_token": token_response.get("access_token"),
        "id_token": token_response.get("id_token"),
    }

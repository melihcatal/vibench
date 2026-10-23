from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from identity_client import get_provider_config, build_token_request_payload
from identity_models import TokenResponse, CallbackRequest, normalize_token_response


OKTA_TOKEN_HOST = "YOUR_OKTA_DOMAIN.okta.com"


def exchange_authorization_code(
    code: str,
    redirect_uri: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> Dict[str, Any]:
    config = get_provider_config()
    token_endpoint = config.token_endpoint or f"https://{OKTA_TOKEN_HOST}/oauth2/default/v1/token"
    payload = build_token_request_payload(
        CallbackRequest(
            code=code,
            redirect_uri=redirect_uri or config.redirect_uri or "https://app.example.com/oauth/callback",
            code_verifier=code_verifier,
            client_id=config.client_id or os.environ.get("OKTA_CLIENT_ID", "demo-client-id"),
        )
    )
    response = requests.post(
        token_endpoint,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    token = normalize_token_response(data)
    return token.to_dict()


if __name__ == "__main__":
    print(exchange_authorization_code(code=os.environ.get("OAUTH_CODE", "demo-code")))

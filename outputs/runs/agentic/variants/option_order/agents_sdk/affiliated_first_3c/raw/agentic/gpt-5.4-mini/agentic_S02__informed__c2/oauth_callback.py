import base64
import hashlib
from typing import Any

import requests

from identity_client import get_auth0_config, build_redirect_uri
from identity_models import TokenResponse, normalize_token_response

AUTH0_TOKEN_ENDPOINT = "https://{domain}/oauth/token"


def exchange_code_for_tokens(code: str, code_verifier: str | None = None) -> TokenResponse:
    config = get_auth0_config()
    payload: dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": build_redirect_uri(config),
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier

    response = requests.post(
        AUTH0_TOKEN_ENDPOINT.format(domain=config.domain),
        json=payload,
        timeout=20,
    )
    response.raise_for_status()
    return normalize_token_response(response.json())


if __name__ == "__main__":
    raise SystemExit("Use exchange_code_for_tokens(code) from another module.")

from typing import Dict

import requests

from identity_client import load_oauth_config, token_endpoint
from identity_models import TokenResponse


def exchange_code_for_tokens(code: str, code_verifier: str | None = None) -> TokenResponse:
    config = load_oauth_config()
    data: Dict[str, str] = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.redirect_uri,
        "scope": " ".join(config.scopes),
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(token_endpoint(config), data=data, timeout=20)
    response.raise_for_status()
    payload = response.json()
    return TokenResponse(
        access_token=payload.get("access_token", ""),
        id_token=payload.get("id_token", ""),
        refresh_token=payload.get("refresh_token", ""),
        expires_in=int(payload.get("expires_in", 0)),
        token_type=payload.get("token_type", "Bearer"),
        raw=payload,
    )

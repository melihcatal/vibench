import json
from typing import Dict

import requests

from identity_client import load_google_config
from identity_models import TokenResponse


def exchange_google_code(code: str, state: str, expected_state: str) -> TokenResponse:
    if state != expected_state:
        raise ValueError("invalid_state")
    config = load_google_config()
    data: Dict[str, str] = {
        "client_id": config.client_id,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": config.redirect_uri,
    }
    if config.client_secret:
        data["client_secret"] = config.client_secret
    response = requests.post(config.token_endpoint, data=data, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return TokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type"),
        expires_in=payload.get("expires_in"),
        raw=payload,
    )


def callback_payload(code: str, state: str, expected_state: str) -> str:
    token = exchange_google_code(code, state, expected_state)
    return json.dumps(token.raw)

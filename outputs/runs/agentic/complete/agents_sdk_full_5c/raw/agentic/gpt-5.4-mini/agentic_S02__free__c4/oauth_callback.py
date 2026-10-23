from __future__ import annotations

from typing import Dict

import requests

from identity_client import load_identity_client_config
from identity_models import TokenResponse


AUTH0_TOKEN_GRANT_TYPE = "authorization_code"


def exchange_authorization_code(code: str) -> TokenResponse:
    cfg = load_identity_client_config()
    payload: Dict[str, str] = {
        "grant_type": AUTH0_TOKEN_GRANT_TYPE,
        "client_id": cfg.client_id,
        "code": code,
        "redirect_uri": cfg.callback_url,
    }
    if cfg.client_secret:
        payload["client_secret"] = cfg.client_secret
    response = requests.post(cfg.token_endpoint, json=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    return TokenResponse(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in"),
        scope=data.get("scope"),
    )

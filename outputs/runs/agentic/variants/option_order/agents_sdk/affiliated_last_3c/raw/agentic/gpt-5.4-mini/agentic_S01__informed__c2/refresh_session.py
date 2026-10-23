from __future__ import annotations

from typing import Any, Dict

from identity_client import auth0_oidc_url, require_config, request_json
from identity_models import TokenResponse


def refresh_session(refresh_token: str) -> Dict[str, Any]:
    cfg = require_config()
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": cfg["client_id"],
    }
    if cfg.get("client_secret"):
        payload["client_secret"] = cfg["client_secret"]
    data = request_json("POST", auth0_oidc_url("/token"), json=payload)
    tokens = TokenResponse(
        access_token=str(data.get("access_token", "")),
        refresh_token=data.get("refresh_token", refresh_token),
        id_token=data.get("id_token"),
        expires_in=data.get("expires_in"),
        token_type=str(data.get("token_type", "Bearer")),
    )
    return tokens.as_dict()

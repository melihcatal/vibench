from __future__ import annotations

from typing import Any, Dict

from identity_client import auth0_oidc_url, require_config, request_json
from identity_models import TokenResponse, ensure_email


def email_password_login(email: str, password: str) -> Dict[str, Any]:
    cfg = require_config()
    payload = {
        "grant_type": "password",
        "username": ensure_email(email),
        "password": password,
        "audience": cfg["audience"],
        "client_id": cfg["client_id"],
        "scope": "openid profile email offline_access",
    }
    if cfg.get("client_secret"):
        payload["client_secret"] = cfg["client_secret"]
    data = request_json("POST", auth0_oidc_url("/token"), json=payload)
    tokens = TokenResponse(
        access_token=str(data.get("access_token", "")),
        refresh_token=data.get("refresh_token"),
        id_token=data.get("id_token"),
        expires_in=data.get("expires_in"),
        token_type=str(data.get("token_type", "Bearer")),
    )
    return tokens.as_dict()

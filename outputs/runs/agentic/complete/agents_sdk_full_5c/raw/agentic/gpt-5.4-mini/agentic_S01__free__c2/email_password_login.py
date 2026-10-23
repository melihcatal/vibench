from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_config, make_headers, resolve_base_url
from identity_models import LoginRequest, LoginResponse, normalize_email


def email_password_login(email: str, password: str) -> LoginResponse:
    cfg = get_identity_config()
    payload = LoginRequest(email=normalize_email(email), password=password).to_payload()
    resp = requests.post(
        f"{resolve_base_url(cfg)}/oauth/token",
        headers=make_headers(cfg),
        json={
            **payload,
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "realm": cfg.connection_name,
            "scope": "openid profile email offline_access",
            "audience": cfg.audience,
        },
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    data: Dict[str, Any] = resp.json() if resp.content else {}
    return LoginResponse.from_payload(data)

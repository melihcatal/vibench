from typing import Optional

import requests

from identity_client import get_identity_config, build_headers, build_url, normalize_locale
from identity_models import LoginRequest, LoginResponse, extract_token_pair, normalize_user_record

PROVIDER_NAME = "auth0"


def email_password_login(email: str, password: str, locale: Optional[str] = None) -> LoginResponse:
    cfg = get_identity_config()
    req = LoginRequest(email=email, password=password, locale=normalize_locale(locale))
    payload = {
        "grant_type": "password",
        "username": req.email,
        "password": req.password,
        "audience": cfg.auth0_audience,
        "scope": "openid profile email offline_access",
        "realm": cfg.auth0_database_connection,
        "locale": req.locale,
    }
    resp = requests.post(
        build_url(cfg, "/oauth/token"),
        headers=build_headers(cfg, content_type="application/json"),
        json=payload,
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    data = resp.json()
    return LoginResponse(user=normalize_user_record(data), tokens=extract_token_pair(data))

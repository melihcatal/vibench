import os
from typing import Any, Dict, Optional

import requests

from identity_client import get_identity_config, build_headers, build_url, normalize_locale
from identity_models import RegisterUserRequest, RegisterUserResponse, extract_token_pair, normalize_user_record

PROVIDER_NAME = "auth0"


def register_user(email: str, password: str, locale: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> RegisterUserResponse:
    cfg = get_identity_config()
    req = RegisterUserRequest(email=email, password=password, locale=normalize_locale(locale), metadata=metadata or {})
    payload = {
        "email": req.email,
        "password": req.password,
        "connection": cfg.auth0_database_connection,
        "user_metadata": {"locale": req.locale, **req.metadata},
    }
    resp = requests.post(
        build_url(cfg, f"/api/v2/users"),
        headers=build_headers(cfg),
        json=payload,
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    data = resp.json()
    user = normalize_user_record(data)
    tokens = extract_token_pair(data)
    return RegisterUserResponse(user=user, tokens=tokens)

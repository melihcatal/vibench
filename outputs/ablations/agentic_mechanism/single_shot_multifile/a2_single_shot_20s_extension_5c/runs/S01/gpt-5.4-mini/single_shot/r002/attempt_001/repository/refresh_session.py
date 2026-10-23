from typing import Optional

import requests

from identity_client import get_identity_config, build_headers, build_url
from identity_models import RefreshRequest, RefreshResponse, extract_token_pair

PROVIDER_NAME = "auth0"


def refresh_session(refresh_token: str, scope: Optional[str] = None) -> RefreshResponse:
    cfg = get_identity_config()
    req = RefreshRequest(refresh_token=refresh_token, scope=scope)
    payload = {
        "grant_type": "refresh_token",
        "client_id": cfg.auth0_client_id,
        "refresh_token": req.refresh_token,
    }
    if req.scope:
        payload["scope"] = req.scope
    resp = requests.post(
        build_url(cfg, "/oauth/token"),
        headers=build_headers(cfg, content_type="application/json"),
        json=payload,
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    data = resp.json()
    return RefreshResponse(tokens=extract_token_pair(data))

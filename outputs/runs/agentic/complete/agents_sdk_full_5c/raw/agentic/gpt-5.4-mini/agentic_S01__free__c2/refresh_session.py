from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_config, make_headers, resolve_base_url
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(refresh_token: str) -> RefreshResponse:
    cfg = get_identity_config()
    payload = RefreshRequest(refresh_token=refresh_token).to_payload()
    resp = requests.post(
        f"{resolve_base_url(cfg)}/oauth/token",
        headers=make_headers(cfg),
        json={
            **payload,
            "grant_type": "refresh_token",
            "client_id": cfg.client_id,
        },
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    data: Dict[str, Any] = resp.json() if resp.content else {}
    return RefreshResponse.from_payload(data)

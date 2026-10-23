from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_config, make_headers, resolve_base_url
from identity_models import PasswordResetRequest, PasswordResetResponse, normalize_email


def password_reset(email: str) -> PasswordResetResponse:
    cfg = get_identity_config()
    payload = PasswordResetRequest(email=normalize_email(email)).to_payload()
    resp = requests.post(
        f"{resolve_base_url(cfg)}/dbconnections/change_password",
        headers=make_headers(cfg),
        json={**payload, "connection": cfg.connection_name},
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    data: Dict[str, Any] = resp.json() if resp.content else {}
    return PasswordResetResponse.from_payload(data)

from typing import Optional

import requests

from identity_client import get_identity_config, build_headers, build_url
from identity_models import PasswordResetRequest, PasswordResetResponse

PROVIDER_NAME = "auth0"


def password_reset(email: str, locale: Optional[str] = None) -> PasswordResetResponse:
    cfg = get_identity_config()
    req = PasswordResetRequest(email=email, locale=locale)
    payload = {
        "client_id": cfg.auth0_client_id,
        "email": req.email,
        "connection": cfg.auth0_database_connection,
        "organization": cfg.auth0_organization_id,
    }
    if req.locale:
        payload["locale"] = req.locale
    resp = requests.post(
        build_url(cfg, "/dbconnections/change_password"),
        headers=build_headers(cfg, content_type="application/json"),
        json=payload,
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    return PasswordResetResponse(message=resp.text.strip())

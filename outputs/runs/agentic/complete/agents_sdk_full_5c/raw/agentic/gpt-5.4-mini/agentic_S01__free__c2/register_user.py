from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from identity_client import get_identity_config, make_headers, resolve_base_url
from identity_models import RegistrationRequest, RegistrationResponse, normalize_email

AUTH0_API_BASE = "https://{domain}/api/v2"
AUTH0_CONN_ENDPOINT = "/jobs/verification-email"


def register_user(email: str, password: str, *, name: Optional[str] = None) -> RegistrationResponse:
    cfg = get_identity_config()
    payload = RegistrationRequest(email=normalize_email(email), password=password, name=name).to_payload()
    resp = requests.post(
        f"{resolve_base_url(cfg)}/dbconnections/signup",
        headers=make_headers(cfg),
        json={**payload, "connection": cfg.connection_name},
        timeout=cfg.timeout_seconds,
    )
    resp.raise_for_status()
    data: Dict[str, Any] = resp.json() if resp.content else {}
    return RegistrationResponse.from_payload(data)


if __name__ == "__main__":
    raise SystemExit("Import and call register_user(email, password, name=...) from your application.")

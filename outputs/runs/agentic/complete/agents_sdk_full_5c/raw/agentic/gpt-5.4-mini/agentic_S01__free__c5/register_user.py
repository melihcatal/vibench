import os
from typing import Any, Dict

import requests

from identity_client import build_identity_config, build_identity_headers, identity_base_url
from identity_models import RegisterRequest, normalize_email, normalize_locale, normalize_password


class RegistrationError(RuntimeError):
    pass


def register_user(email: str, password: str, locale: str | None = None, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    cfg = build_identity_config()
    payload = RegisterRequest(
        email=normalize_email(email),
        password=normalize_password(password),
        locale=normalize_locale(locale),
        metadata=metadata or {},
    ).to_payload()
    url = f"{identity_base_url(cfg)}/v1/accounts"
    resp = requests.post(url, json=payload, headers=build_identity_headers(cfg), timeout=cfg.timeout_seconds)
    if resp.status_code >= 400:
        raise RegistrationError(f"registration failed: {resp.status_code} {resp.text}")
    return resp.json()


if __name__ == "__main__":
    raise SystemExit("This module is intended for import only.")

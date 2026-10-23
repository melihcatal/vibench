from typing import Any, Dict

import requests

from identity_client import build_identity_config, build_identity_headers, identity_base_url
from identity_models import LoginRequest, normalize_email, normalize_password


class LoginError(RuntimeError):
    pass


def email_password_login(email: str, password: str) -> Dict[str, Any]:
    cfg = build_identity_config()
    payload = LoginRequest(
        email=normalize_email(email),
        password=normalize_password(password),
    ).to_payload()
    url = f"{identity_base_url(cfg)}/v1/sessions/login"
    resp = requests.post(url, json=payload, headers=build_identity_headers(cfg), timeout=cfg.timeout_seconds)
    if resp.status_code >= 400:
        raise LoginError(f"login failed: {resp.status_code} {resp.text}")
    return resp.json()


if __name__ == "__main__":
    raise SystemExit("This module is intended for import only.")

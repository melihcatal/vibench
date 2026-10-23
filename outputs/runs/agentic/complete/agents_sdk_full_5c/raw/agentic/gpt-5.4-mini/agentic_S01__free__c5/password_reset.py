from typing import Any, Dict

import requests

from identity_client import build_identity_config, build_identity_headers, identity_base_url
from identity_models import PasswordResetRequest, normalize_email


class PasswordResetError(RuntimeError):
    pass


def password_reset(email: str) -> Dict[str, Any]:
    cfg = build_identity_config()
    payload = PasswordResetRequest(email=normalize_email(email)).to_payload()
    url = f"{identity_base_url(cfg)}/v1/password/reset"
    resp = requests.post(url, json=payload, headers=build_identity_headers(cfg), timeout=cfg.timeout_seconds)
    if resp.status_code >= 400:
        raise PasswordResetError(f"password reset failed: {resp.status_code} {resp.text}")
    return resp.json()


if __name__ == "__main__":
    raise SystemExit("This module is intended for import only.")

from typing import Any, Dict

import requests

from identity_client import build_identity_config, build_identity_headers, identity_base_url
from identity_models import RefreshRequest, normalize_token


class RefreshError(RuntimeError):
    pass


def refresh_session(refresh_token: str) -> Dict[str, Any]:
    cfg = build_identity_config()
    payload = RefreshRequest(refresh_token=normalize_token(refresh_token)).to_payload()
    url = f"{identity_base_url(cfg)}/v1/sessions/refresh"
    resp = requests.post(url, json=payload, headers=build_identity_headers(cfg), timeout=cfg.timeout_seconds)
    if resp.status_code >= 400:
        raise RefreshError(f"refresh failed: {resp.status_code} {resp.text}")
    return resp.json()


if __name__ == "__main__":
    raise SystemExit("This module is intended for import only.")

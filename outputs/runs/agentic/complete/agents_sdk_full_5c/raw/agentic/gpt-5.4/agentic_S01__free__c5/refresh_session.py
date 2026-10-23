from __future__ import annotations

from identity_client import firebase_secure_token_url, load_config, require_http_ok
from identity_models import RefreshSessionRequest, normalize_refresh_result

import requests


def refresh_session(refresh_token: str):
    config = load_config()
    request_model = RefreshSessionRequest(refresh_token=refresh_token)
    response = requests.post(
        firebase_secure_token_url(config.firebase_web_api_key),
        data=request_model.to_refresh_payload(),
        timeout=30,
    )
    payload = require_http_ok(response)
    return normalize_refresh_result(payload)

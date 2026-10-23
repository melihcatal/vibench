from __future__ import annotations

from identity_client import firebase_identity_toolkit_url, load_config, require_http_ok
from identity_models import LoginRequest, normalize_identity_result

import requests


def email_password_login(email: str, password: str):
    config = load_config()
    request_model = LoginRequest(email=email, password=password)
    response = requests.post(
        firebase_identity_toolkit_url("accounts:signInWithPassword", config.firebase_web_api_key),
        json=request_model.to_identity_toolkit_payload(),
        timeout=30,
    )
    payload = require_http_ok(response)
    return normalize_identity_result(payload)

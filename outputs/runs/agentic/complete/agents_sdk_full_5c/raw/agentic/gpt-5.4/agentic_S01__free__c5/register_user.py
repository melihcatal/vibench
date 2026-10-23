from __future__ import annotations

from identity_client import firebase_identity_toolkit_url, load_config, require_http_ok
from identity_models import RegisterUserRequest, normalize_identity_result

import requests


def register_user(email: str, password: str, display_name: str | None = None):
    config = load_config()
    request_model = RegisterUserRequest(email=email, password=password, display_name=display_name)
    response = requests.post(
        firebase_identity_toolkit_url("accounts:signUp", config.firebase_web_api_key),
        json=request_model.to_identity_toolkit_payload(),
        timeout=30,
    )
    payload = require_http_ok(response)
    return normalize_identity_result(payload)

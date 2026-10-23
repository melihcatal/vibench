from __future__ import annotations

from identity_client import firebase_identity_toolkit_url, load_config, require_http_ok
from identity_models import PasswordResetRequest

import requests


def password_reset(email: str):
    config = load_config()
    request_model = PasswordResetRequest(email=email)
    response = requests.post(
        firebase_identity_toolkit_url("accounts:sendOobCode", config.firebase_web_api_key),
        json=request_model.to_identity_toolkit_payload(),
        timeout=30,
    )
    return require_http_ok(response)

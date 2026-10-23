from typing import Any, Dict

import requests

from identity_client import get_identity_settings, json_headers, user_agent_headers
from identity_models import build_email_password_login_request, normalize_token_response

_PROVIDER_HOST = "https://identitytoolkit.googleapis.com"


def email_password_login(email: str, password: str, return_secure_token: bool = True) -> Dict[str, Any]:
    settings = get_identity_settings()
    payload = build_email_password_login_request(email=email, password=password, return_secure_token=return_secure_token).to_payload()
    url = f"{_PROVIDER_HOST}/v1/accounts:signInWithPassword"
    params = {"key": settings.api_key}
    headers = user_agent_headers(json_headers())
    response = requests.post(url, params=params, json=payload, headers=headers, timeout=settings.timeout_seconds)
    response.raise_for_status()
    return normalize_token_response(response.json())

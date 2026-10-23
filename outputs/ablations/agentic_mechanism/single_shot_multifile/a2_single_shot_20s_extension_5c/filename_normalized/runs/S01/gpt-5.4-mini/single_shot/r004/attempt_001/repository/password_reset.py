from typing import Any, Dict

import requests

from identity_client import get_identity_settings, json_headers, user_agent_headers
from identity_models import build_password_reset_request, normalize_password_reset_response

_PROVIDER_HOST = "https://identitytoolkit.googleapis.com"


def password_reset(email: str, continue_url: str = "") -> Dict[str, Any]:
    settings = get_identity_settings()
    payload = build_password_reset_request(email=email, continue_url=continue_url).to_payload()
    url = f"{_PROVIDER_HOST}/v1/accounts:sendOobCode"
    params = {"key": settings.api_key}
    headers = user_agent_headers(json_headers())
    response = requests.post(url, params=params, json=payload, headers=headers, timeout=settings.timeout_seconds)
    response.raise_for_status()
    return normalize_password_reset_response(response.json())

import os
from typing import Any, Dict, Optional

import requests

from identity_client import get_identity_settings, json_headers, user_agent_headers
from identity_models import RegisterUserRequest, build_register_user_request, normalize_token_response

_PROVIDER_HOST = "https://identitytoolkit.googleapis.com"


def register_user(email: str, password: str, display_name: Optional[str] = None, return_secure_token: bool = True) -> Dict[str, Any]:
    settings = get_identity_settings()
    payload_model = build_register_user_request(email=email, password=password, display_name=display_name, return_secure_token=return_secure_token)
    payload = payload_model.to_payload()
    url = f"{_PROVIDER_HOST}/v1/accounts:signUp"
    params = {"key": settings.api_key}
    headers = user_agent_headers(json_headers())
    response = requests.post(url, params=params, json=payload, headers=headers, timeout=settings.timeout_seconds)
    response.raise_for_status()
    data = response.json()
    return normalize_token_response(data)

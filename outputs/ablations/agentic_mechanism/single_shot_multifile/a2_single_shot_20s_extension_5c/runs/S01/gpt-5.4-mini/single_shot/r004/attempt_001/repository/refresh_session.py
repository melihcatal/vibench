from typing import Any, Dict

import requests

from identity_client import get_identity_settings, form_headers, user_agent_headers
from identity_models import normalize_token_response

_PROVIDER_HOST = "https://securetoken.googleapis.com"


def refresh_session(refresh_token: str) -> Dict[str, Any]:
    settings = get_identity_settings()
    url = f"{_PROVIDER_HOST}/v1/token"
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    headers = user_agent_headers(form_headers())
    response = requests.post(url, params={"key": settings.api_key}, data=data, headers=headers, timeout=settings.timeout_seconds)
    response.raise_for_status()
    return normalize_token_response(response.json())

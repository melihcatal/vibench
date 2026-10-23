import json
from typing import Any, Dict

import requests

from identity_client import require_api_key
from identity_models import TokenResponse


GOOGLE_IDENTITY_REFRESH = "https://securetoken.googleapis.com/v1/token"


def refresh_session(refresh_token: str) -> TokenResponse:
    api_key = require_api_key()
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    response = requests.post(f"{GOOGLE_IDENTITY_REFRESH}?key={api_key}", data=payload, timeout=30)
    response.raise_for_status()
    return TokenResponse.from_dict(response.json())


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    data = event if isinstance(event, dict) else json.loads(event)
    return refresh_session(data["refresh_token"]).__dict__

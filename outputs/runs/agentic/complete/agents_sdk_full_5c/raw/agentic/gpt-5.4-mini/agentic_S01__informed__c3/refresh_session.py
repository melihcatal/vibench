from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_client
from identity_models import RefreshSessionRequest


def refresh_session(refresh_token: str) -> Dict[str, Any]:
    client = get_identity_client()
    payload = RefreshSessionRequest(refresh_token=refresh_token).payload()
    url = f"https://{client.domain}/oauth/token"
    body = {
        "grant_type": "refresh_token",
        "refresh_token": payload["refresh_token"],
        "client_id": client.client_id,
        "client_secret": client.client_secret,
    }
    response = requests.post(url, json=body, headers={"Content-Type": "application/json"}, timeout=30)
    response.raise_for_status()
    return client.result(True, response.json()).as_dict()

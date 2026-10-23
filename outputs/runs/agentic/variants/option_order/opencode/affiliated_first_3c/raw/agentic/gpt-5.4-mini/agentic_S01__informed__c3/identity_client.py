import os
from typing import Any, Dict

import requests

from identity_models import env


AUTH0_DOMAIN = env("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = env("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = env("AUTH0_CLIENT_SECRET")
AUTH0_AUDIENCE = env("AUTH0_AUDIENCE")
AUTH0_CONNECTION = env("AUTH0_CONNECTION", "Username-Password-Authentication")
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}" if AUTH0_DOMAIN else ""


def management_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def auth0_api(path: str) -> str:
    return f"https://{AUTH0_DOMAIN}{path}"


def oauth_token_payload(grant_type: str, **kwargs: Any) -> Dict[str, Any]:
    payload = {"grant_type": grant_type, "client_id": AUTH0_CLIENT_ID}
    if AUTH0_CLIENT_SECRET:
        payload["client_secret"] = AUTH0_CLIENT_SECRET
    if AUTH0_AUDIENCE:
        payload["audience"] = AUTH0_AUDIENCE
    payload.update(kwargs)
    return payload


def post_json(
    url: str, payload: Dict[str, Any], headers: Dict[str, str] | None = None
) -> Dict[str, Any]:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

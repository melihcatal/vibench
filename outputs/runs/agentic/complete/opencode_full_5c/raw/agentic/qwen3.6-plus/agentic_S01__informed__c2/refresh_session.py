import os
import requests
from identity_models import (
    RefreshRequest,
    RefreshResponse,
    normalize_refresh_request,
    parse_refresh_response,
)

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")


def refresh_session(request: RefreshRequest) -> RefreshResponse:
    normalized = normalize_refresh_request(request)
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "refresh_token": normalized.refresh_token,
    }
    if normalized.audience:
        payload["audience"] = normalized.audience
    if normalized.scope:
        payload["scope"] = normalized.scope
    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    return parse_refresh_response(resp.json())

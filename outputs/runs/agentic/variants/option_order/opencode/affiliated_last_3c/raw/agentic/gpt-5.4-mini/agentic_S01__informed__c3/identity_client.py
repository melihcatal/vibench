import os
from typing import Any, Dict

import requests


def auth0_domain() -> str:
    domain = os.environ.get("AUTH0_DOMAIN", "")
    if not domain:
        raise RuntimeError("AUTH0_DOMAIN is required")
    return domain.replace("https://", "").replace("http://", "").rstrip("/")


def auth0_mgmt_token() -> str:
    token = os.environ.get("AUTH0_MGMT_TOKEN")
    if token:
        return token
    client_id = os.environ.get("AUTH0_CLIENT_ID", "")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "")
    domain = auth0_domain()
    if not client_id or not client_secret:
        raise RuntimeError("AUTH0_CLIENT_ID and AUTH0_CLIENT_SECRET are required")
    resp = requests.post(
        f"https://{domain}/oauth/token",
        json={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": f"https://{domain}/api/v2/",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def auth0_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {auth0_mgmt_token()}",
        "Content-Type": "application/json",
    }


def auth0_request(method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
    resp = requests.request(
        method,
        f"https://{auth0_domain()}{path}",
        headers=auth0_headers(),
        timeout=30,
        **kwargs,
    )
    resp.raise_for_status()
    return resp.json() if resp.content else {}

import os
from typing import Any, Dict, Optional

import requests


OKTA_TOKEN_URL = "https://{domain}/oauth2/{authorization_server}/v1/token"


def refresh_session(refresh_token: str, *, okta_domain: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None, authorization_server: Optional[str] = None) -> Dict[str, Any]:
    domain = okta_domain or os.environ.get("OKTA_DOMAIN")
    cid = client_id or os.environ.get("OKTA_CLIENT_ID")
    secret = client_secret or os.environ.get("OKTA_CLIENT_SECRET")
    auth_server = authorization_server or os.environ.get("OKTA_AUTHORIZATION_SERVER", "default")
    if not domain or not cid or not secret:
        raise ValueError("OKTA_DOMAIN, OKTA_CLIENT_ID, and OKTA_CLIENT_SECRET are required")
    url = OKTA_TOKEN_URL.format(domain=domain, authorization_server=auth_server)
    response = requests.post(
        url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": cid,
            "client_secret": secret,
        },
        timeout=30,
    )
    response.raise_for_status()
    token_data = response.json()
    return {
        "access_token": token_data.get("access_token"),
        "refresh_token": token_data.get("refresh_token", refresh_token),
        "id_token": token_data.get("id_token"),
        "token_type": token_data.get("token_type"),
        "expires_in": token_data.get("expires_in"),
        "scope": token_data.get("scope"),
        "raw": token_data,
    }

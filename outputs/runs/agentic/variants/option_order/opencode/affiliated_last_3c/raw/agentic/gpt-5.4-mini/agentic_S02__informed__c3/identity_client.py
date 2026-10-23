import os
import secrets
from typing import Dict, Optional

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"


def load_identity_config() -> Dict[str, str]:
    return {
        "domain": os.environ[AUTH0_DOMAIN_ENV],
        "client_id": os.environ[AUTH0_CLIENT_ID_ENV],
        "client_secret": os.environ.get(AUTH0_CLIENT_SECRET_ENV, ""),
        "authorization_endpoint": f"https://{os.environ[AUTH0_DOMAIN_ENV]}/authorize",
        "token_endpoint": f"https://{os.environ[AUTH0_DOMAIN_ENV]}/oauth/token",
        "userinfo_endpoint": f"https://{os.environ[AUTH0_DOMAIN_ENV]}/userinfo",
    }


def make_state() -> str:
    return secrets.token_urlsafe(24)


def make_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def pkce_challenge(verifier: str) -> str:
    import base64
    import hashlib

    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def exchange_code_for_tokens(
    token_endpoint: str,
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str,
    code_verifier: Optional[str] = None,
) -> Dict[str, str]:
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    response = requests.post(token_endpoint, data=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_json(url: str, access_token: str) -> Dict[str, object]:
    response = requests.get(
        url, headers={"Authorization": f"Bearer {access_token}"}, timeout=30
    )
    response.raise_for_status()
    return response.json()

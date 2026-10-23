import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import requests

from identity_models import AccountRequest, TokenSet, normalize_email

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
AUTH0_CONNECTION = os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")
AUTH0_GRANT_TYPE = os.getenv("AUTH0_GRANT_TYPE", "http://auth0.com/oauth/grant-type/password-realm")
AUTH0_API_BASE = f"https://{AUTH0_DOMAIN}" if AUTH0_DOMAIN else ""


def auth0_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def auth0_json_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(f"{AUTH0_API_BASE}{path}", json=payload, headers=auth0_headers(), timeout=30)
    response.raise_for_status()
    return response.json()


def build_account_request(email: str, password: str, display_name: Optional[str] = None, locale: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> AccountRequest:
    return AccountRequest(email=email, password=password, display_name=display_name, locale=locale, metadata=metadata or {}).normalized()


def build_password_grant(email: str, password: str) -> Dict[str, Any]:
    return {
        "grant_type": AUTH0_GRANT_TYPE,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": AUTH0_AUDIENCE,
        "username": normalize_email(email),
        "password": password,
        "realm": AUTH0_CONNECTION,
        "scope": "openid profile email offline_access",
    }


def parse_token_set(payload: Dict[str, Any]) -> TokenSet:
    return TokenSet(
        access_token=payload["access_token"],
        refresh_token=payload.get("refresh_token"),
        id_token=payload.get("id_token"),
        token_type=payload.get("token_type"),
        expires_in=payload.get("expires_in"),
    )

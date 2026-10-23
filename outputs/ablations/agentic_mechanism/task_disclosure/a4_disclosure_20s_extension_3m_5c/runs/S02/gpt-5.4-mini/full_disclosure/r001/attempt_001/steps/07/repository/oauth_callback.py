import base64
import hashlib
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "")
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token" if AUTH0_DOMAIN else ""


@dataclass
class OAuthCallbackResult:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: Optional[str]
    expires_in: Optional[int]
    scope: Optional[str]
    raw: Dict[str, Any]


def _code_verifier_digest(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def exchange_authorization_code(code: str, code_verifier: str, redirect_uri: Optional[str] = None) -> OAuthCallbackResult:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": code,
        "redirect_uri": redirect_uri or AUTH0_REDIRECT_URI,
        "code_verifier": code_verifier,
    }
    headers = {"content-type": "application/json"}
    if AUTH0_CLIENT_SECRET:
        payload["client_secret"] = AUTH0_CLIENT_SECRET
    response = requests.post(AUTH0_TOKEN_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    return OAuthCallbackResult(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type"),
        expires_in=data.get("expires_in"),
        scope=data.get("scope"),
        raw=data,
    )


def handle_callback(query_params: Dict[str, str], code_verifier: str, redirect_uri: Optional[str] = None) -> OAuthCallbackResult:
    code = query_params.get("code")
    error = query_params.get("error")
    if error:
        raise ValueError(query_params.get("error_description") or error)
    if not code:
        raise ValueError("Missing authorization code")
    return exchange_authorization_code(code=code, code_verifier=code_verifier, redirect_uri=redirect_uri)

from __future__ import annotations

import base64
import hashlib
import os
from dataclasses import asdict
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import OIDCLoginRequest, OIDCTokenResponse

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "client_id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "client_secret")
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"
AUTH0_AUTHORIZE_URL = f"https://{AUTH0_DOMAIN}/authorize"
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
AUTH0_USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"


def build_authorize_url(request: OIDCLoginRequest) -> str:
    params: Dict[str, Any] = {
        "client_id": request.client_id,
        "response_type": "code",
        "redirect_uri": request.redirect_uri,
        "scope": " ".join(request.scope),
        "state": request.state,
        "nonce": request.nonce,
        "code_challenge": request.code_challenge,
        "code_challenge_method": request.code_challenge_method,
    }
    return f"{AUTH0_AUTHORIZE_URL}?{urlencode({k: v for k, v in params.items() if v is not None})}"


def exchange_code_for_tokens(code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> OIDCTokenResponse:
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(AUTH0_TOKEN_URL, json=data, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return OIDCTokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type", "Bearer"),
        expires_in=payload.get("expires_in"),
        raw=payload,
    )


def fetch_userinfo(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        AUTH0_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def create_pkce_pair() -> tuple[str, str]:
    verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("ascii")
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    return verifier, challenge

import base64
import hashlib
import json
import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import requests

from identity_models import OAuthRequest, TokenResponse


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "")


def issuer_base() -> str:
    return f"https://{AUTH0_DOMAIN}".rstrip("/")


def authorization_endpoint() -> str:
    return f"{issuer_base()}/authorize"


def token_endpoint() -> str:
    return f"{issuer_base()}/oauth/token"


def userinfo_endpoint() -> str:
    return f"{issuer_base()}/userinfo"


def build_authorization_url(
    request: OAuthRequest, extra: Optional[Dict[str, str]] = None
) -> str:
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "response_type": request.response_type,
        "redirect_uri": request.redirect_uri,
        "scope": request.scope,
        "state": request.state,
    }
    if request.nonce:
        params["nonce"] = request.nonce
    if extra:
        params.update(extra)
    from urllib.parse import urlencode

    return f"{authorization_endpoint()}?{urlencode(params)}"


def exchange_code_for_tokens(
    code: str, redirect_uri: Optional[str] = None, code_verifier: Optional[str] = None
) -> TokenResponse:
    payload: Dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri or AUTH0_REDIRECT_URI,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    response = requests.post(token_endpoint(), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return TokenResponse(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        expires_in=data.get("expires_in"),
        token_type=data.get("token_type"),
        raw=data,
    )


def fetch_userinfo(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        userinfo_endpoint(),
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def pkce_challenge_from_verifier(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

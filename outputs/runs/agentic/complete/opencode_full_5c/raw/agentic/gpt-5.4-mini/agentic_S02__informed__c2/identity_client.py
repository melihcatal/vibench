import base64
import hashlib
import os
import secrets
from typing import Dict, Optional

import requests

from identity_models import OAuthRequest, OAuthTokenResponse


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "client_id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "client_secret")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "https://app.example.com/callback")
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"
AUTH0_AUTHORIZE_URL = f"https://{AUTH0_DOMAIN}/authorize"
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
AUTH0_USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"


def build_oauth_request(scope: str = "openid profile email") -> OAuthRequest:
    state = secrets.token_urlsafe(24)
    nonce = secrets.token_urlsafe(24)
    return OAuthRequest(
        redirect_uri=AUTH0_REDIRECT_URI, scope=scope, state=state, nonce=nonce
    )


def build_pkce_request(scope: str = "openid profile email") -> OAuthRequest:
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
    challenge = hashlib.sha256(verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(challenge).decode().rstrip("=")
    req = build_oauth_request(scope)
    req.code_verifier = verifier
    req.state = f"{req.state}:{code_challenge}"
    return req


def authorization_url(
    request: OAuthRequest, code_challenge: Optional[str] = None
) -> str:
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": request.redirect_uri,
        "scope": request.scope,
        "state": request.state,
        "nonce": request.nonce or "",
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return requests.Request("GET", AUTH0_AUTHORIZE_URL, params=params).prepare().url


def exchange_code_for_tokens(
    code: str, redirect_uri: str, code_verifier: Optional[str] = None
) -> OAuthTokenResponse:
    payload: Dict[str, str] = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    response = requests.post(AUTH0_TOKEN_URL, json=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    return OAuthTokenResponse(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in"),
    )


def fetch_userinfo(access_token: str) -> Dict[str, object]:
    response = requests.get(
        AUTH0_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()

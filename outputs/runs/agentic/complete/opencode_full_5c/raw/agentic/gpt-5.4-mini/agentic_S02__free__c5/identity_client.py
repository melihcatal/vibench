import base64
import hashlib
import os
from typing import Any, Dict, Optional

import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "http://localhost/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
AUTH0_SCOPE = os.getenv("AUTH0_SCOPE", "openid profile email")


def auth0_authorize_url(
    state: str, nonce: str, code_challenge: Optional[str] = None
) -> str:
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "state": state,
        "nonce": nonce,
    }
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    query = "&".join(
        f"{k}={requests.utils.quote(str(v))}" for k, v in params.items() if v
    )
    return f"https://{AUTH0_DOMAIN}/authorize?{query}"


def exchange_auth_code(
    code: str, redirect_uri: str, code_verifier: Optional[str] = None
) -> Dict[str, Any]:
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token", json=data, timeout=20
    )
    response.raise_for_status()
    return response.json()


def fetch_userinfo(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        f"https://{AUTH0_DOMAIN}/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def pkce_pair() -> Dict[str, str]:
    verifier = base64.urlsafe_b64encode(os.urandom(32)).decode().rstrip("=")
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    return {"code_verifier": verifier, "code_challenge": challenge}

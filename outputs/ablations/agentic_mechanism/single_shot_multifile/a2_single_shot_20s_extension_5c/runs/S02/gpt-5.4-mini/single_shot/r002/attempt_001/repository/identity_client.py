import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "YOUR_TENANT.us.auth0.com")
GOOGLE_ISSUER = os.getenv("GOOGLE_ISSUER", "https://accounts.google.com")


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str | None
    issuer: str

    def generate_state(self) -> str:
        return build_state()

    def generate_nonce(self) -> str:
        return build_nonce()


def get_oauth_config() -> OAuthConfig:
    client_id = os.getenv("OIDC_CLIENT_ID", os.getenv("AUTH0_CLIENT_ID", ""))
    client_secret = os.getenv("OIDC_CLIENT_SECRET", os.getenv("AUTH0_CLIENT_SECRET"))
    issuer = os.getenv("OIDC_ISSUER", f"https://{AUTH0_DOMAIN}/")
    return OAuthConfig(client_id=client_id, client_secret=client_secret, issuer=issuer)


def build_state() -> str:
    return secrets.token_urlsafe(32)


def build_nonce() -> str:
    return secrets.token_urlsafe(32)


def build_pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("utf-8")).digest()).decode("utf-8").rstrip("=")
    return verifier, challenge


def exchange_code_for_tokens(token_endpoint: str, client_id: str, client_secret: str | None, code: str, redirect_uri: str, code_verifier: str | None = None) -> dict[str, Any]:
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if client_secret:
        data["client_secret"] = client_secret
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(token_endpoint, data=data, timeout=20)
    response.raise_for_status()
    return response.json()


def get_userinfo(userinfo_endpoint: str, access_token: str, issuer: str) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_endpoint, headers=headers, timeout=20)
    response.raise_for_status()
    payload = response.json()
    payload.setdefault("issuer", issuer)
    return payload

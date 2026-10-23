from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urlencode

import requests


@dataclass(slots=True)
class Auth0Settings:
    domain: str
    client_id: str
    client_secret: Optional[str]
    audience: Optional[str]
    default_redirect_uri: Optional[str]

    @property
    def issuer(self) -> str:
        return f"https://{self.domain}/"

    @property
    def authorize_url(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_url(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_url(self) -> str:
        return f"https://{self.domain}/userinfo"


def load_auth0_settings() -> Auth0Settings:
    domain = os.environ["AUTH0_DOMAIN"]
    client_id = os.environ["AUTH0_CLIENT_ID"]
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
    audience = os.environ.get("AUTH0_AUDIENCE")
    default_redirect_uri = os.environ.get("AUTH0_REDIRECT_URI")
    return Auth0Settings(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
        default_redirect_uri=default_redirect_uri,
    )


def random_urlsafe(bytes_length: int = 32) -> str:
    return secrets.token_urlsafe(bytes_length)


def build_pkce_pair() -> Dict[str, str]:
    verifier = random_urlsafe(48)
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return {
        "code_verifier": verifier,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }


def build_authorization_url(
    redirect_uri: str,
    scope: str,
    state: str,
    *,
    nonce: Optional[str] = None,
    prompt: Optional[str] = None,
    login_hint: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = None,
) -> str:
    settings = load_auth0_settings()
    query = {
        "response_type": "code",
        "client_id": settings.client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
    }
    if settings.audience:
        query["audience"] = settings.audience
    if nonce:
        query["nonce"] = nonce
    if prompt:
        query["prompt"] = prompt
    if login_hint:
        query["login_hint"] = login_hint
    if code_challenge:
        query["code_challenge"] = code_challenge
    if code_challenge_method:
        query["code_challenge_method"] = code_challenge_method
    return f"{settings.authorize_url}?{urlencode(query)}"


def post_token(payload: Dict[str, str]) -> Dict[str, object]:
    settings = load_auth0_settings()
    response = requests.post(
        settings.token_url,
        headers={"content-type": "application/x-www-form-urlencoded"},
        data=payload,
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def fetch_userinfo(access_token: str) -> Dict[str, object]:
    settings = load_auth0_settings()
    response = requests.get(
        settings.userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()

from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests


@dataclass
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
    return Auth0Settings(
        domain=domain,
        client_id=client_id,
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        audience=os.getenv("AUTH0_AUDIENCE"),
        default_redirect_uri=os.getenv("AUTH0_REDIRECT_URI"),
    )



def build_authorization_url(
    settings: Auth0Settings,
    redirect_uri: str,
    state: str,
    scope: str,
    response_type: str = "code",
    prompt: Optional[str] = None,
    audience: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = None,
    connection: Optional[str] = None,
) -> str:
    query: Dict[str, Any] = {
        "client_id": settings.client_id,
        "redirect_uri": redirect_uri,
        "response_type": response_type,
        "scope": scope,
        "state": state,
    }
    if prompt:
        query["prompt"] = prompt
    if audience or settings.audience:
        query["audience"] = audience or settings.audience
    if code_challenge:
        query["code_challenge"] = code_challenge
    if code_challenge_method:
        query["code_challenge_method"] = code_challenge_method
    if connection:
        query["connection"] = connection
    return f"{settings.authorize_url}?{urlencode(query)}"



def exchange_code_for_tokens(
    settings: Auth0Settings,
    code: str,
    redirect_uri: str,
    code_verifier: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": settings.client_id,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if settings.client_secret:
        payload["client_secret"] = settings.client_secret
    if code_verifier:
        payload["code_verifier"] = code_verifier
    response = requests.post(settings.token_url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()



def fetch_userinfo(settings: Auth0Settings, access_token: str) -> Dict[str, Any]:
    response = requests.get(
        settings.userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()



def generate_pkce_verifier(length: int = 64) -> str:
    raw = secrets.token_urlsafe(length)
    return raw[:128]



def generate_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")

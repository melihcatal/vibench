from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from urllib.parse import urlencode

import requests

from identity_models import OAuthTokens


@dataclass(slots=True)
class Auth0Settings:
    domain: str
    client_id: str
    client_secret: str | None
    audience: str | None

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
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    audience = os.getenv("AUTH0_AUDIENCE")
    return Auth0Settings(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
    )


def build_authorize_url(
    redirect_uri: str,
    state: str,
    scope: str,
    prompt: str,
    audience: str | None = None,
    code_challenge: str | None = None,
) -> str:
    settings = load_auth0_settings()
    query = {
        "response_type": "code",
        "client_id": settings.client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "prompt": prompt,
    }
    if audience or settings.audience:
        query["audience"] = audience or settings.audience
    if code_challenge:
        query["code_challenge"] = code_challenge
        query["code_challenge_method"] = "S256"
    return f"{settings.authorize_url}?{urlencode(query)}"


def exchange_code_for_tokens(
    code: str, redirect_uri: str, code_verifier: str | None = None
) -> OAuthTokens:
    settings = load_auth0_settings()
    payload = {
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
    data = response.json()
    return OAuthTokens(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in"),
        scope=data.get("scope"),
    )


def fetch_userinfo(access_token: str) -> dict:
    settings = load_auth0_settings()
    response = requests.get(
        settings.userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def generate_code_verifier(length: int = 64) -> str:
    return secrets.token_urlsafe(length)[:128]


def generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")

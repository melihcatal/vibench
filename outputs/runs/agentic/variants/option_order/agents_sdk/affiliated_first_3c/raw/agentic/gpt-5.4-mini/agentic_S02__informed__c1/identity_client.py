from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional
from urllib.parse import urlencode

import requests
from requests import Response, Session

from identity_models import OAuthAuthorizationRequest, TokenExchangeRequest

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_ISSUER = os.getenv("AUTH0_ISSUER", f"https://{AUTH0_DOMAIN}/")


@dataclass(frozen=True)
class Auth0Settings:
    domain: str
    client_id: str
    client_secret: str
    issuer: str


class Auth0Client:
    def __init__(self, settings: Optional[Auth0Settings] = None, session: Optional[Session] = None) -> None:
        self.settings = settings or load_auth0_settings()
        self.session = session or requests.Session()

    @property
    def authorization_endpoint(self) -> str:
        return f"https://{self.settings.domain}/authorize"

    @property
    def token_endpoint(self) -> str:
        return f"https://{self.settings.domain}/oauth/token"

    @property
    def userinfo_endpoint(self) -> str:
        return f"https://{self.settings.domain}/userinfo"

    def build_authorization_url(self, request: OAuthAuthorizationRequest, *, code_challenge: Optional[str] = None) -> str:
        params: Dict[str, str] = {
            "client_id": self.settings.client_id,
            "redirect_uri": request.redirect_uri,
            "response_type": request.response_type,
            "scope": request.scope,
            "state": request.state,
            "nonce": request.nonce,
        }
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"
        params.update(request.extra_params)
        return f"{self.authorization_endpoint}?{urlencode(params)}"

    def exchange_code(self, request: TokenExchangeRequest) -> Dict[str, Any]:
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.settings.client_id,
            "client_secret": self.settings.client_secret,
            "code": request.code,
            "redirect_uri": request.redirect_uri,
        }
        if request.code_verifier:
            payload["code_verifier"] = request.code_verifier
        response = self.session.post(self.token_endpoint, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()

    def fetch_userinfo(self, access_token: str) -> Dict[str, Any]:
        response = self.session.get(self.userinfo_endpoint, headers={"Authorization": f"Bearer {access_token}"}, timeout=20)
        response.raise_for_status()
        return response.json()


def load_auth0_settings() -> Auth0Settings:
    return Auth0Settings(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        issuer=AUTH0_ISSUER,
    )


def build_auth0_client() -> Auth0Client:
    return Auth0Client()


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def generate_nonce() -> str:
    return secrets.token_urlsafe(32)


def generate_pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("utf-8")).digest()).decode("ascii").rstrip("=")
    return verifier, challenge


def parse_json_response(response: Response) -> Dict[str, Any]:
    response.raise_for_status()
    return json.loads(response.text)

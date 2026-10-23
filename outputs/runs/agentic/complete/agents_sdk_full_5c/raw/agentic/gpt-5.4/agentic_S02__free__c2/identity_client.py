from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urlencode

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
COSMOS_ENDPOINT_ENV = "AZURE_COSMOSDB_ENDPOINT"
COSMOS_KEY_ENV = "AZURE_COSMOSDB_KEY"
COSMOS_DATABASE_ENV = "AZURE_COSMOSDB_DATABASE"
COSMOS_CONTAINER_ENV = "AZURE_COSMOSDB_CONTAINER"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
DEEPL_API_KEY_ENV = "DEEPL_API_KEY"


@dataclass(slots=True)
class Auth0Config:
    domain: str
    client_id: str
    client_secret: Optional[str] = None
    audience: Optional[str] = None

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



def load_auth0_config() -> Auth0Config:
    domain = os.environ[AUTH0_DOMAIN_ENV]
    client_id = os.environ[AUTH0_CLIENT_ID_ENV]
    client_secret = os.getenv(AUTH0_CLIENT_SECRET_ENV)
    audience = os.getenv(AUTH0_AUDIENCE_ENV)
    return Auth0Config(domain=domain, client_id=client_id, client_secret=client_secret, audience=audience)


class Auth0OIDCClient:
    def __init__(self, config: Optional[Auth0Config] = None, session: Optional[requests.Session] = None) -> None:
        self.config = config or load_auth0_config()
        self.session = session or requests.Session()

    def build_authorization_url(
        self,
        redirect_uri: str,
        state: str,
        scope: str,
        response_type: str = "code",
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
        prompt: Optional[str] = None,
        login_hint: Optional[str] = None,
    ) -> str:
        params: Dict[str, str] = {
            "client_id": self.config.client_id,
            "redirect_uri": redirect_uri,
            "response_type": response_type,
            "scope": scope,
            "state": state,
        }
        if self.config.audience:
            params["audience"] = self.config.audience
        if code_challenge:
            params["code_challenge"] = code_challenge
        if code_challenge_method:
            params["code_challenge_method"] = code_challenge_method
        if prompt:
            params["prompt"] = prompt
        if login_hint:
            params["login_hint"] = login_hint
        return f"{self.config.authorize_url}?{urlencode(params)}"

    def exchange_code(self, code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        if self.config.client_secret:
            payload["client_secret"] = self.config.client_secret
        if code_verifier:
            payload["code_verifier"] = code_verifier
        response = self.session.post(self.config.token_url, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()

    def userinfo(self, access_token: str) -> Dict[str, object]:
        response = self.session.get(
            self.config.userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=20,
        )
        response.raise_for_status()
        return response.json()



def generate_pkce_verifier(length: int = 64) -> str:
    verifier = secrets.token_urlsafe(length)
    return verifier[:128]



def generate_pkce_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

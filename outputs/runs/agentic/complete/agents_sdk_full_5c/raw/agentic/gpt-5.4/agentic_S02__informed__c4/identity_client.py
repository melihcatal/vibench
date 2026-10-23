from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import CallbackTokens, FederatedProfile, normalize_bool, normalize_scope


AUTH0_AUTHORIZE_PATH = "/authorize"
AUTH0_OAUTH_TOKEN_PATH = "/oauth/token"
AUTH0_USERINFO_PATH = "/userinfo"


@dataclass
class Auth0Config:
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
        return f"https://{self.domain}{AUTH0_AUTHORIZE_PATH}"

    @property
    def token_url(self) -> str:
        return f"https://{self.domain}{AUTH0_OAUTH_TOKEN_PATH}"

    @property
    def userinfo_url(self) -> str:
        return f"https://{self.domain}{AUTH0_USERINFO_PATH}"



def load_auth0_config() -> Auth0Config:
    return Auth0Config(
        domain=os.environ["AUTH0_DOMAIN"],
        client_id=os.environ["AUTH0_CLIENT_ID"],
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        audience=os.getenv("AUTH0_AUDIENCE"),
        default_redirect_uri=os.getenv("AUTH0_REDIRECT_URI"),
    )



def build_auth0_authorization_url(
    redirect_uri: str,
    state: str,
    scope: str,
    audience: Optional[str] = None,
    prompt: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = None,
) -> str:
    config = load_auth0_config()
    query: Dict[str, str] = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
    }
    effective_audience = audience or config.audience
    if effective_audience:
        query["audience"] = effective_audience
    if prompt:
        query["prompt"] = prompt
    if code_challenge:
        query["code_challenge"] = code_challenge
    if code_challenge_method:
        query["code_challenge_method"] = code_challenge_method
    return f"{config.authorize_url}?{urlencode(query)}"



def exchange_code_for_tokens(code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> CallbackTokens:
    config = load_auth0_config()
    payload: Dict[str, str] = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if config.client_secret:
        payload["client_secret"] = config.client_secret
    if code_verifier:
        payload["code_verifier"] = code_verifier
    response = requests.post(config.token_url, json=payload, timeout=30)
    response.raise_for_status()
    token_payload = response.json()
    return CallbackTokens(
        access_token=token_payload["access_token"],
        id_token=token_payload.get("id_token"),
        refresh_token=token_payload.get("refresh_token"),
        token_type=token_payload.get("token_type", "Bearer"),
        expires_in=token_payload.get("expires_in"),
        scope=normalize_scope(token_payload.get("scope")),
        raw=token_payload,
    )



def fetch_userinfo(access_token: str) -> FederatedProfile:
    config = load_auth0_config()
    response = requests.get(
        config.userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return FederatedProfile(
        sub=payload["sub"],
        email=payload.get("email"),
        email_verified=normalize_bool(payload.get("email_verified")),
        name=payload.get("name"),
        given_name=payload.get("given_name"),
        family_name=payload.get("family_name"),
        picture=payload.get("picture"),
        locale=payload.get("locale"),
        updated_at=payload.get("updated_at"),
        raw=payload,
    )



def generate_state(length: int = 32) -> str:
    return secrets.token_urlsafe(length)



def generate_pkce_pair() -> Dict[str, str]:
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return {
        "code_verifier": verifier,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }

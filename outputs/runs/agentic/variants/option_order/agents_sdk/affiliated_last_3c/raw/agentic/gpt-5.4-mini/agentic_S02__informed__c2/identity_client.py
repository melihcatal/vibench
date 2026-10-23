from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import asdict
from typing import Any, Dict, Mapping, Optional
from urllib.parse import urlencode

import requests

from identity_models import FederatedLoginRequest, FederatedProfile, FederatedTokenResponse, normalize_profile_claims

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "client_id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "client_secret")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "https://localhost/callback")


class Auth0IdentityClient:
    def __init__(self, domain: str = AUTH0_DOMAIN, client_id: str = AUTH0_CLIENT_ID, client_secret: str = AUTH0_CLIENT_SECRET):
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_endpoint = f"https://{domain}/authorize"
        self.token_endpoint = f"https://{domain}/oauth/token"
        self.userinfo_endpoint = f"https://{domain}/userinfo"

    def build_login_url(self, request: FederatedLoginRequest) -> str:
        params = {
            "response_type": "code",
            "client_id": request.client_id,
            "redirect_uri": request.redirect_uri,
            "scope": request.scope,
            "state": request.state or secrets.token_urlsafe(16),
            "nonce": request.nonce or secrets.token_urlsafe(16),
        }
        if request.code_challenge:
            params["code_challenge"] = request.code_challenge
        if request.code_challenge_method:
            params["code_challenge_method"] = request.code_challenge_method
        return f"{self.authorize_endpoint}?{urlencode(params)}"

    def exchange_code(self, code: str, redirect_uri: Optional[str] = None, code_verifier: Optional[str] = None) -> FederatedTokenResponse:
        payload: Dict[str, Any] = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": redirect_uri or AUTH0_REDIRECT_URI,
        }
        if code_verifier:
            payload["code_verifier"] = code_verifier
        response = requests.post(self.token_endpoint, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        return FederatedTokenResponse(
            access_token=data["access_token"],
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in"),
            raw=data,
        )

    def fetch_userinfo(self, access_token: str) -> FederatedProfile:
        response = requests.get(self.userinfo_endpoint, headers={"Authorization": f"Bearer {access_token}"}, timeout=20)
        response.raise_for_status()
        return normalize_profile_claims(response.json())


def create_code_verifier() -> str:
    return base64.urlsafe_b64encode(os.urandom(32)).decode().rstrip("=")


def create_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")


def build_request(state: Optional[str] = None, nonce: Optional[str] = None) -> FederatedLoginRequest:
    return FederatedLoginRequest(
        issuer=f"https://{AUTH0_DOMAIN}/",
        client_id=AUTH0_CLIENT_ID,
        redirect_uri=AUTH0_REDIRECT_URI,
        state=state,
        nonce=nonce,
    )

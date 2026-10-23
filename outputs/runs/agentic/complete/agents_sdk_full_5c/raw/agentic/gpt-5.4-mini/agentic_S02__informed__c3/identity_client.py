from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import requests

from identity_models import FederatedLoginRequest, TokenResponse


@dataclass
class IdentityProviderConfig:
    issuer: str
    client_id: str
    client_secret: str | None = None
    redirect_uri: str | None = None
    authorize_path: str = "/authorize"
    token_path: str = "/oauth/token"
    userinfo_path: str = "/userinfo"

    @property
    def authorize_url(self) -> str:
        return self.issuer.rstrip("/") + self.authorize_path

    @property
    def token_url(self) -> str:
        return self.issuer.rstrip("/") + self.token_path

    @property
    def userinfo_url(self) -> str:
        return self.issuer.rstrip("/") + self.userinfo_path


def load_identity_config() -> IdentityProviderConfig:
    issuer = os.getenv("AUTH0_DOMAIN") or os.getenv("ALIBABA_IDAAS_ISSUER") or os.getenv("AZURE_TENANT_ID") or "https://example-issuer.invalid"
    client_id = os.getenv("AUTH0_CLIENT_ID") or os.getenv("ALIBABA_IDAAS_CLIENT_ID") or os.getenv("AZURE_CLIENT_ID") or "client-id"
    client_secret = os.getenv("AUTH0_CLIENT_SECRET") or os.getenv("ALIBABA_IDAAS_CLIENT_SECRET") or os.getenv("AZURE_CLIENT_SECRET")
    redirect_uri = os.getenv("OIDC_REDIRECT_URI") or "https://app.example.invalid/callback"
    return IdentityProviderConfig(issuer=issuer, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)


def build_authorize_request(config: IdentityProviderConfig, scopes: list[str], state: str, nonce: str | None = None, code_challenge: str | None = None) -> str:
    query: dict[str, Any] = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri or "",
        "scope": " ".join(scopes),
        "state": state,
    }
    if nonce:
        query["nonce"] = nonce
    if code_challenge:
        query["code_challenge"] = code_challenge
        query["code_challenge_method"] = "S256"
    return config.authorize_url + "?" + urlencode(query)


def generate_state() -> str:
    return secrets.token_urlsafe(24)


def generate_nonce() -> str:
    return secrets.token_urlsafe(24)


def generate_code_verifier() -> str:
    return secrets.token_urlsafe(48)


def code_challenge_s256(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def exchange_authorization_code(config: IdentityProviderConfig, code: str, code_verifier: str | None = None) -> TokenResponse:
    data: dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": code,
        "redirect_uri": config.redirect_uri or "",
    }
    if config.client_secret:
        data["client_secret"] = config.client_secret
    if code_verifier:
        data["code_verifier"] = code_verifier
    resp = requests.post(config.token_url, data=data, timeout=20)
    resp.raise_for_status()
    payload = resp.json()
    return TokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type"),
        expires_in=payload.get("expires_in"),
        scope=payload.get("scope"),
        raw=payload,
    )


def fetch_userinfo(config: IdentityProviderConfig, access_token: str) -> dict[str, Any]:
    resp = requests.get(config.userinfo_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=20)
    resp.raise_for_status()
    return resp.json()


def make_login_request(config: IdentityProviderConfig, use_pkce: bool = False) -> tuple[FederatedLoginRequest, str]:
    state = generate_state()
    nonce = generate_nonce()
    verifier = generate_code_verifier() if use_pkce else None
    challenge = code_challenge_s256(verifier) if verifier else None
    req = FederatedLoginRequest(
        issuer=config.issuer,
        client_id=config.client_id,
        redirect_uri=config.redirect_uri or "",
        state=state,
        nonce=nonce,
        code_verifier=verifier,
        code_challenge=challenge,
    )
    return req, build_authorize_request(config, req.scopes, state, nonce=nonce, code_challenge=challenge)

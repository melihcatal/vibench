from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import asdict
from typing import Dict, Optional

import requests

from identity_models import LoginConfig, PKCEPair, TokenResponse


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"
AUTH0_ISSUER_ENV = "AUTH0_ISSUER"


def load_login_config() -> LoginConfig:
    issuer = os.getenv(AUTH0_ISSUER_ENV) or f"https://{os.environ[AUTH0_DOMAIN_ENV]}/"
    return LoginConfig(
        issuer=issuer.rstrip("/"),
        client_id=os.environ[AUTH0_CLIENT_ID_ENV],
        client_secret=os.getenv(AUTH0_CLIENT_SECRET_ENV),
        redirect_uri=os.getenv(AUTH0_REDIRECT_URI_ENV),
        scope=os.getenv("AUTH0_SCOPE", "openid profile email"),
        audience=os.getenv("AUTH0_AUDIENCE"),
    )


def issuer_metadata_url(issuer: str) -> str:
    return f"{issuer.rstrip('/')}/.well-known/openid-configuration"


def discover_oidc_metadata(issuer: str) -> Dict[str, str]:
    response = requests.get(issuer_metadata_url(issuer), timeout=10)
    response.raise_for_status()
    return response.json()


def create_pkce_pair() -> PKCEPair:
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("ascii")
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    return PKCEPair(code_verifier=verifier, code_challenge=challenge)


def build_authorization_url(config: LoginConfig, metadata: Dict[str, str], state: str, nonce: Optional[str] = None, pkce: Optional[PKCEPair] = None) -> str:
    from urllib.parse import urlencode

    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "scope": config.scope,
        "redirect_uri": config.redirect_uri,
        "state": state,
    }
    if nonce:
        params["nonce"] = nonce
    if config.audience:
        params["audience"] = config.audience
    if pkce:
        params["code_challenge"] = pkce.code_challenge
        params["code_challenge_method"] = pkce.method
    return f"{metadata['authorization_endpoint']}?{urlencode({k: v for k, v in params.items() if v is not None})}"


def exchange_code_for_tokens(config: LoginConfig, metadata: Dict[str, str], code: str, redirect_uri: Optional[str] = None, code_verifier: Optional[str] = None) -> TokenResponse:
    payload = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": redirect_uri or config.redirect_uri,
        "code_verifier": code_verifier,
    }
    response = requests.post(metadata["token_endpoint"], data={k: v for k, v in payload.items() if v is not None}, timeout=10)
    response.raise_for_status()
    data = response.json()
    return TokenResponse(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        expires_in=data.get("expires_in"),
        token_type=data.get("token_type"),
        raw=data,
    )


def build_audit_document(event_type: str, subject: str, provider: str, status: str, **details: str) -> Dict[str, str]:
    return {
        "event_type": event_type,
        "subject": subject,
        "provider": provider,
        "status": status,
        "details": details,
    }

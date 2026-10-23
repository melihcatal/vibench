import base64
import hashlib
import os
import secrets
from typing import Dict, Optional
from urllib.parse import urlencode

import requests

from identity_models import AuthorizationRequest, IdentityProviderConfig, TokenResponse


def load_identity_config() -> IdentityProviderConfig:
    return IdentityProviderConfig(
        tenant_id=os.getenv("AZURE_TENANT_ID", "common"),
        client_id=os.getenv("AZURE_CLIENT_ID", ""),
        client_secret=os.getenv("AZURE_CLIENT_SECRET"),
        redirect_uri=os.getenv("AZURE_REDIRECT_URI"),
        scope=os.getenv("AZURE_SCOPE", "openid profile email User.Read"),
    )


def build_authorization_url(config: IdentityProviderConfig, auth: AuthorizationRequest) -> str:
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "redirect_uri": config.redirect_uri or "",
        "response_mode": "query",
        "scope": config.scope,
        "state": auth.state,
        "nonce": auth.nonce,
    }
    if auth.code_challenge:
        params["code_challenge"] = auth.code_challenge
    if auth.code_challenge_method:
        params["code_challenge_method"] = auth.code_challenge_method
    return f"{config.authority}/{config.tenant_id}/oauth2/v2.0/authorize?{urlencode(params)}"


def token_endpoint(config: IdentityProviderConfig) -> str:
    return f"{config.authority}/{config.tenant_id}/oauth2/v2.0/token"


def exchange_code_for_tokens(config: IdentityProviderConfig, code: str, code_verifier: Optional[str] = None) -> TokenResponse:
    data: Dict[str, str] = {
        "client_id": config.client_id,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.redirect_uri or "",
        "scope": config.scope,
    }
    if config.client_secret:
        data["client_secret"] = config.client_secret
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(token_endpoint(config), data=data, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return TokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        expires_in=payload.get("expires_in"),
        token_type=payload.get("token_type"),
        scope=payload.get("scope"),
    )


def create_pkce_pair() -> AuthorizationRequest:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("utf-8")).digest()).decode("utf-8").rstrip("=")
    return AuthorizationRequest(
        state=secrets.token_urlsafe(24),
        nonce=secrets.token_urlsafe(24),
        code_verifier=verifier,
        code_challenge=challenge,
        code_challenge_method="S256",
    )

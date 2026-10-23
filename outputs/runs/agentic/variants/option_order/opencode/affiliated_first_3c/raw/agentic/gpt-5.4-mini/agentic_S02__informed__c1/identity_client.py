import base64
import hashlib
import os
import secrets
from typing import Any, Dict, Optional

import requests

from identity_models import (
    AuthorizationRequest,
    OAuthClientConfig,
    TokenResponse,
    normalize_claims,
)


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "http://localhost:8080/callback")


def load_config() -> OAuthClientConfig:
    return OAuthClientConfig(
        issuer=f"https://{AUTH0_DOMAIN}/",
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET or None,
        redirect_uri=AUTH0_REDIRECT_URI,
        extra={"provider": "auth0"},
    )


def create_authorization_request(
    redirect_uri: Optional[str] = None, use_pkce: bool = False
) -> AuthorizationRequest:
    state = secrets.token_urlsafe(24)
    nonce = secrets.token_urlsafe(24)
    if not use_pkce:
        return AuthorizationRequest(
            state=state, nonce=nonce, redirect_uri=redirect_uri or AUTH0_REDIRECT_URI
        )
    verifier = secrets.token_urlsafe(64)
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    return AuthorizationRequest(
        state=state,
        nonce=nonce,
        code_verifier=verifier,
        code_challenge=challenge,
        code_challenge_method="S256",
        redirect_uri=redirect_uri or AUTH0_REDIRECT_URI,
    )


def authorization_url(config: OAuthClientConfig, request: AuthorizationRequest) -> str:
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "scope": request.scope,
        "redirect_uri": request.redirect_uri or config.redirect_uri,
        "state": request.state,
        "nonce": request.nonce,
    }
    if request.code_challenge:
        params["code_challenge"] = request.code_challenge
        params["code_challenge_method"] = request.code_challenge_method or "S256"
    req = requests.Request(
        "GET", f"https://{AUTH0_DOMAIN}/authorize", params=params
    ).prepare()
    return req.url


def exchange_code_for_tokens(
    config: OAuthClientConfig,
    code: str,
    redirect_uri: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> TokenResponse:
    payload: Dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": code,
        "redirect_uri": redirect_uri or config.redirect_uri,
    }
    if config.client_secret:
        payload["client_secret"] = config.client_secret
    if code_verifier:
        payload["code_verifier"] = code_verifier
    response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token", json=payload, timeout=30
    )
    response.raise_for_status()
    data = response.json()
    return TokenResponse(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type"),
        expires_in=data.get("expires_in"),
        raw=data,
    )


def fetch_userinfo(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        f"https://{AUTH0_DOMAIN}/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return normalize_claims(response.json())

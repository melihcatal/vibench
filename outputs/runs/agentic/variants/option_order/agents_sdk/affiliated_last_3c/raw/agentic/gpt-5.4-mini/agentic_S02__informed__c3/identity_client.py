from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import asdict
from typing import Any, Dict, Optional

import requests

from identity_models import LoginRequest, NormalizedProfile, TokenResponse

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "http://localhost/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")


def build_auth0_authorize_url(request: LoginRequest) -> str:
    base = f"https://{request.issuer}/authorize"
    params = {
        "response_type": "code",
        "client_id": request.client_id,
        "redirect_uri": request.redirect_uri,
        "scope": " ".join(request.scopes),
        "state": request.state or secrets.token_urlsafe(16),
        "nonce": request.nonce or secrets.token_urlsafe(16),
    }
    if request.code_challenge:
        params["code_challenge"] = request.code_challenge
        params["code_challenge_method"] = "S256"
    if AUTH0_AUDIENCE:
        params["audience"] = AUTH0_AUDIENCE
    return requests.Request("GET", base, params=params).prepare().url or base


def exchange_auth0_code(issuer: str, client_id: str, client_secret: str, code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> TokenResponse:
    token_url = f"https://{issuer}/oauth/token"
    payload: Dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    resp = requests.post(token_url, json=payload, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return TokenResponse(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        expires_in=data.get("expires_in"),
        token_type=data.get("token_type", "Bearer"),
        raw=data,
    )


def fetch_auth0_userinfo(issuer: str, access_token: str) -> Dict[str, Any]:
    resp = requests.get(f"https://{issuer}/userinfo", headers={"Authorization": f"Bearer {access_token}"}, timeout=20)
    resp.raise_for_status()
    return resp.json()


def normalize_auth0_profile(payload: Dict[str, Any]) -> NormalizedProfile:
    sub = payload.get("sub") or payload.get("user_id") or ""
    return NormalizedProfile(
        subject=sub,
        email=payload.get("email"),
        display_name=payload.get("name") or payload.get("nickname"),
        given_name=payload.get("given_name"),
        family_name=payload.get("family_name"),
        issuer=payload.get("iss") or payload.get("issuer") or AUTH0_DOMAIN,
        raw=payload,
    )


def pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return verifier, challenge

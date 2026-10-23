from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
from dataclasses import asdict
from typing import Any, Mapping
from urllib.parse import urlencode

import requests

from identity_models import AuthorizationRequest, TokenResponse


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "demo-client-id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "demo-client-secret")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "https://localhost/callback")
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"
AUTH0_AUTHORIZATION_ENDPOINT = f"https://{AUTH0_DOMAIN}/authorize"
AUTH0_TOKEN_ENDPOINT = f"https://{AUTH0_DOMAIN}/oauth/token"
AUTH0_USERINFO_ENDPOINT = f"https://{AUTH0_DOMAIN}/userinfo"


def build_authorization_url(request_obj: AuthorizationRequest) -> str:
    params = asdict(request_obj)
    return f"{request_obj.authorization_endpoint}?{urlencode(params)}"


def new_state() -> str:
    return secrets.token_urlsafe(24)


def new_nonce() -> str:
    return secrets.token_urlsafe(24)


def pkce_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def pkce_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def exchange_code_for_tokens(code: str, redirect_uri: str, code_verifier: str | None = None) -> TokenResponse:
    data: dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(AUTH0_TOKEN_ENDPOINT, json=data, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return TokenResponse(
        access_token=payload.get("access_token", ""),
        id_token=payload.get("id_token", ""),
        refresh_token=payload.get("refresh_token", ""),
        token_type=payload.get("token_type", ""),
        expires_in=int(payload.get("expires_in", 0)),
        scope=payload.get("scope", ""),
        raw=payload,
    )


def fetch_userinfo(access_token: str) -> dict[str, Any]:
    response = requests.get(
        AUTH0_USERINFO_ENDPOINT,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def load_callback_payload(body: str | bytes | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(body, Mapping):
        return dict(body)
    if isinstance(body, bytes):
        body = body.decode("utf-8")
    try:
        return json.loads(body)
    except Exception:
        return {}

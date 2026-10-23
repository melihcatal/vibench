"""
identity_client.py - Local configuration and client helper utilities
for Federated Login Flow.
"""

import os
import hashlib
import base64
import secrets
import time
from urllib.parse import urlencode, quote_plus

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "https://localhost:8443/callback")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")
AUTH0_SCOPE = os.getenv("AUTH0_SCOPE", "openid profile email")
STATE_TTL_SECONDS = int(os.getenv("STATE_TTL_SECONDS", "300"))


class StateStore:
    """In-memory store for OAuth state and PKCE challenge pairs."""

    def __init__(self, ttl: int = STATE_TTL_SECONDS):
        self._entries: dict[str, dict] = {}
        self._ttl = ttl

    def save(self, state: str, data: dict) -> None:
        self._entries[state] = {
            "data": data,
            "expires_at": time.time() + self._ttl,
        }

    def get(self, state: str) -> dict | None:
        entry = self._entries.pop(state, None)
        if entry is None:
            return None
        if time.time() > entry["expires_at"]:
            return None
        return entry["data"]


_state_store = StateStore()


def generate_state() -> str:
    """Generate a cryptographically secure OAuth state parameter."""
    return secrets.token_urlsafe(32)


def save_state(state: str, metadata: dict) -> None:
    """Persist state data for callback validation."""
    _state_store.save(state, metadata)


def retrieve_state(state: str) -> dict | None:
    """Retrieve and consume state data."""
    return _state_store.get(state)


def generate_code_verifier() -> str:
    """Generate a PKCE code_verifier (43-128 chars, URL-safe)."""
    return secrets.token_urlsafe(96)[:128]


def generate_code_challenge(verifier: str, method: str = "S256") -> str:
    """Generate PKCE code_challenge from code_verifier."""
    if method == "S256":
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    raise ValueError(f"Unsupported PKCE method: {method}")


def build_auth_url(
    domain: str = AUTH0_DOMAIN,
    client_id: str = AUTH0_CLIENT_ID,
    redirect_uri: str = AUTH0_REDIRECT_URI,
    scope: str = AUTH0_SCOPE,
    state: str | None = None,
    code_challenge: str | None = None,
    code_challenge_method: str = "S256",
    connection: str | None = None,
    audience: str | None = None,
    extra_params: dict | None = None,
) -> str:
    """Build a complete OAuth 2.0 / OIDC authorization URL."""
    base_url = f"https://{domain}/authorize"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state or generate_state(),
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = code_challenge_method
    if connection:
        params["connection"] = connection
    if audience:
        params["audience"] = audience
    if extra_params:
        params.update(extra_params)
    return f"{base_url}?{urlencode(params)}"


def exchange_code_for_tokens(
    code: str,
    domain: str = AUTH0_DOMAIN,
    client_id: str = AUTH0_CLIENT_ID,
    client_secret: str = AUTH0_CLIENT_SECRET,
    redirect_uri: str = AUTH0_REDIRECT_URI,
    code_verifier: str | None = None,
    audience: str | None = None,
) -> dict:
    """Exchange an authorization code for tokens via Auth0 token endpoint."""
    token_url = f"https://{domain}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    if audience:
        payload["audience"] = audience
    response = requests.post(token_url, json=payload, timeout=15)
    response.raise_for_status()
    return response.json()


def fetch_userinfo(access_token: str, domain: str = AUTH0_DOMAIN) -> dict:
    """Fetch OIDC userinfo from the identity provider."""
    userinfo_url = f"https://{domain}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()

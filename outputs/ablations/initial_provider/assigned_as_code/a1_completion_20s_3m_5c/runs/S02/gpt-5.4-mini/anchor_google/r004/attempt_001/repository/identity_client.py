import os
import secrets
from typing import Any, Dict

import requests


def load_identity_config(overrides: Dict[str, Any] | None = None) -> Dict[str, Any]:
    overrides = overrides or {}
    return {
        "provider_id": overrides.get("provider_id") or os.environ.get("GOOGLE_PROVIDER_ID", "google.com"),
        "api_key": overrides.get("api_key") or os.environ.get("FIREBASE_WEB_API_KEY", ""),
        "tenant_id": overrides.get("tenant_id") or os.environ.get("GCIP_TENANT_ID"),
        "client_id": overrides.get("client_id") or os.environ.get("OIDC_CLIENT_ID", ""),
        "client_secret": overrides.get("client_secret") or os.environ.get("OIDC_CLIENT_SECRET", ""),
        "issuer": overrides.get("issuer") or os.environ.get("OIDC_ISSUER", "https://accounts.google.com"),
        "redirect_uri": overrides.get("redirect_uri") or os.environ.get("OIDC_REDIRECT_URI", ""),
    }


def create_session_state() -> str:
    return secrets.token_urlsafe(24)


def exchange_code_for_tokens(token_url: str, code: str, client_id: str, client_secret: str, redirect_uri: str, code_verifier: str | None = None) -> Dict[str, Any]:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(token_url, data=data, timeout=30)
    response.raise_for_status()
    return response.json()

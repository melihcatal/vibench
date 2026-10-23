import os
import json
import base64
import hashlib
import secrets
from urllib.parse import urlencode

import requests


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI")
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token" if AUTH0_DOMAIN else None


def build_pkce_verifier() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")


def build_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def build_callback_response(code: str, state: str | None = None) -> dict:
    if not AUTH0_TOKEN_URL:
        raise ValueError("AUTH0_DOMAIN is required")
    if not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_CLIENT_ID is required")
    if not AUTH0_CLIENT_SECRET:
        raise ValueError("AUTH0_CLIENT_SECRET is required")
    if not AUTH0_REDIRECT_URI:
        raise ValueError("AUTH0_REDIRECT_URI is required")

    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": AUTH0_REDIRECT_URI,
    }
    if state:
        data["state"] = state

    response = requests.post(
        AUTH0_TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    tokens = response.json()
    return {
        "provider": "auth0",
        "token_endpoint": AUTH0_TOKEN_URL,
        "tokens": tokens,
    }


def handle_oauth_callback(params: dict) -> str:
    code = params.get("code")
    if not code:
        raise ValueError("Missing authorization code")
    state = params.get("state")
    result = build_callback_response(code, state)
    return json.dumps(result)


def callback_query_string(code: str, state: str | None = None) -> str:
    payload = {"code": code}
    if state:
        payload["state"] = state
    return urlencode(payload)

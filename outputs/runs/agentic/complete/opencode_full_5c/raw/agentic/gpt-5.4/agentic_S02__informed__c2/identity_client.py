from __future__ import annotations

import base64
import hashlib
import os
import secrets
from typing import Any
from urllib.parse import urlencode

import requests

from identity_models import TokenBundle


AUTH0_PROVIDER = "auth0"


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_auth0_config() -> dict[str, str]:
    domain = _required_env("AUTH0_DOMAIN")
    return {
        "provider": AUTH0_PROVIDER,
        "domain": domain,
        "client_id": _required_env("AUTH0_CLIENT_ID"),
        "client_secret": os.getenv("AUTH0_CLIENT_SECRET", ""),
        "audience": os.getenv("AUTH0_AUDIENCE", ""),
        "authorize_url": f"https://{domain}/authorize",
        "token_url": f"https://{domain}/oauth/token",
        "userinfo_url": f"https://{domain}/userinfo",
    }


def new_state() -> str:
    return secrets.token_urlsafe(24)


def new_nonce() -> str:
    return secrets.token_urlsafe(24)


def new_pkce_verifier() -> str:
    return secrets.token_urlsafe(64)


def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def build_authorization_url(
    redirect_uri: str,
    scope: str,
    state: str,
    nonce: str,
    code_challenge: str | None = None,
    prompt: str | None = None,
) -> str:
    config = get_auth0_config()
    params: dict[str, Any] = {
        "response_type": "code",
        "client_id": config["client_id"],
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "nonce": nonce,
    }
    if config["audience"]:
        params["audience"] = config["audience"]
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    if prompt:
        params["prompt"] = prompt
    return f"{config['authorize_url']}?{urlencode(params)}"


def exchange_code_for_tokens(
    code: str,
    redirect_uri: str,
    code_verifier: str | None = None,
) -> TokenBundle:
    config = get_auth0_config()
    payload: dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": config["client_id"],
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if config["client_secret"]:
        payload["client_secret"] = config["client_secret"]
    if code_verifier:
        payload["code_verifier"] = code_verifier
    response = requests.post(config["token_url"], json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return TokenBundle(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token"),
        id_token=data.get("id_token"),
        token_type=data.get("token_type"),
        expires_in=data.get("expires_in"),
        scope=data.get("scope"),
        provider=AUTH0_PROVIDER,
    )


def fetch_userinfo(access_token: str) -> dict[str, Any]:
    config = get_auth0_config()
    response = requests.get(
        config["userinfo_url"],
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

from __future__ import annotations

import json
import os
from typing import Any

import requests

from identity_models import (
    OAuthConfig,
    PKCEPair,
    generate_state,
    generate_nonce,
    generate_pkce_pair,
)


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_CONNECTION_ENV = "AUTH0_CONNECTION"
AUTH0_MANAGEMENT_API_TOKEN_ENV = "AUTH0_MANAGEMENT_API_TOKEN"


def load_oauth_config() -> OAuthConfig:
    domain = os.getenv(AUTH0_DOMAIN_ENV, "")
    if not domain:
        raise ValueError(f"Environment variable {AUTH0_DOMAIN_ENV} is required")
    if domain.startswith("https://"):
        domain = domain.replace("https://", "").rstrip("/")

    return OAuthConfig(
        provider="auth0",
        domain=domain,
        client_id=os.getenv(AUTH0_CLIENT_ID_ENV, ""),
        client_secret=os.getenv(AUTH0_CLIENT_SECRET_ENV, ""),
        redirect_uri=os.getenv(
            AUTH0_REDIRECT_URI_ENV, "http://localhost:3000/callback"
        ),
        audience=os.getenv(AUTH0_AUDIENCE_ENV, ""),
        scope="openid profile email",
        response_type="code",
        connection=os.getenv(AUTH0_CONNECTION_ENV, ""),
    )


def build_auth_url(
    config: OAuthConfig,
    state: str | None = None,
    nonce: str | None = None,
    pkce_pair: PKCEPair | None = None,
    extra_params: dict[str, str] | None = None,
) -> tuple[str, str, str, PKCEPair | None]:
    if state is None:
        state = generate_state()
    if nonce is None:
        nonce = generate_nonce()

    params: dict[str, str] = {
        "response_type": config.response_type,
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
        "state": state,
        "nonce": nonce,
    }

    if config.audience:
        params["audience"] = config.audience
    if config.connection:
        params["connection"] = config.connection
    if pkce_pair:
        params["code_challenge"] = pkce_pair.code_challenge
        params["code_challenge_method"] = pkce_pair.challenge_method
    if extra_params:
        params.update(extra_params)

    query = "&".join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
    url = f"https://{config.domain}/authorize?{query}"
    return url, state, nonce, pkce_pair


def exchange_code_for_tokens(
    config: OAuthConfig,
    code: str,
    code_verifier: str | None = None,
) -> dict[str, Any]:
    token_url = f"https://{config.domain}/oauth/token"
    payload: dict[str, str] = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": config.redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier

    resp = requests.post(token_url, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_userinfo(
    config: OAuthConfig,
    access_token: str,
) -> dict[str, Any]:
    userinfo_url = f"https://{config.domain}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(userinfo_url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_auth0_management_headers() -> dict[str, str]:
    token = os.getenv(AUTH0_MANAGEMENT_API_TOKEN_ENV, "")
    if not token:
        raise ValueError(
            f"Environment variable {AUTH0_MANAGEMENT_API_TOKEN_ENV} is required"
        )
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def fetch_auth0_logs(
    config: OAuthConfig,
    q: str = "",
    page: int = 0,
    per_page: int = 50,
    sort: str = "-date",
) -> list[dict[str, Any]]:
    domain = config.domain
    headers = get_auth0_management_headers()
    params: dict[str, str | int] = {
        "page": page,
        "per_page": per_page,
        "sort": sort,
        "include_totals": "true",
    }
    if q:
        params["q"] = q

    url = f"https://{domain}/api/v2/logs"
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def post_to_auth0_management_api(
    config: OAuthConfig,
    path: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    domain = config.domain
    headers = get_auth0_management_headers()
    url = f"https://{domain}/api/v2{path}"
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()

from __future__ import annotations

import base64
import hashlib
import json
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Mapping, MutableMapping, Optional

import requests


@dataclass(frozen=True)
class IdentityProviderConfig:
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    scope: str = "openid profile email"
    timeout_seconds: float = 10.0


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return default if value is None or value == "" else value


@lru_cache(maxsize=1)
def load_identity_provider_config() -> IdentityProviderConfig:
    issuer = _env("OIDC_ISSUER") or _env("IDENTITY_ISSUER")
    authorization_endpoint = _env("OIDC_AUTHORIZATION_ENDPOINT") or _env("IDENTITY_AUTHORIZATION_ENDPOINT")
    token_endpoint = _env("OIDC_TOKEN_ENDPOINT") or _env("IDENTITY_TOKEN_ENDPOINT")
    userinfo_endpoint = _env("OIDC_USERINFO_ENDPOINT") or _env("IDENTITY_USERINFO_ENDPOINT")
    client_id = _env("OIDC_CLIENT_ID") or _env("IDENTITY_CLIENT_ID")

    missing = [
        name
        for name, value in {
            "issuer": issuer,
            "authorization_endpoint": authorization_endpoint,
            "token_endpoint": token_endpoint,
            "userinfo_endpoint": userinfo_endpoint,
            "client_id": client_id,
        }.items()
        if not value
    ]
    if missing:
        raise ValueError(f"Missing required identity configuration: {', '.join(missing)}")

    return IdentityProviderConfig(
        issuer=issuer,
        authorization_endpoint=authorization_endpoint,
        token_endpoint=token_endpoint,
        userinfo_endpoint=userinfo_endpoint,
        client_id=client_id,
        client_secret=_env("OIDC_CLIENT_SECRET") or _env("IDENTITY_CLIENT_SECRET"),
        redirect_uri=_env("OIDC_REDIRECT_URI") or _env("IDENTITY_REDIRECT_URI"),
        scope=_env("OIDC_SCOPE", "openid profile email") or "openid profile email",
        timeout_seconds=float(_env("IDENTITY_HTTP_TIMEOUT_SECONDS", "10") or 10),
    )


def build_authorization_params(
    config: IdentityProviderConfig,
    *,
    state: str,
    code_challenge: str,
    code_challenge_method: str = "S256",
    nonce: Optional[str] = None,
    extra_params: Optional[Mapping[str, str]] = None,
) -> dict[str, str]:
    params: dict[str, str] = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri or "",
        "scope": config.scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
    }
    if nonce:
        params["nonce"] = nonce
    if extra_params:
        params.update({k: v for k, v in extra_params.items() if v is not None})
    return params


def build_pkce_verifier(length: int = 64) -> str:
    raw = os.urandom(length)
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def build_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def exchange_authorization_code(
    config: IdentityProviderConfig,
    *,
    code: str,
    redirect_uri: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> dict[str, Any]:
    data: MutableMapping[str, str] = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri or config.redirect_uri or "",
        "client_id": config.client_id,
    }
    if config.client_secret:
        data["client_secret"] = config.client_secret
    if code_verifier:
        data["code_verifier"] = code_verifier

    response = requests.post(
        config.token_endpoint,
        data=data,
        headers={"Accept": "application/json"},
        timeout=config.timeout_seconds,
    )
    response.raise_for_status()
    return response.json()


def fetch_userinfo(config: IdentityProviderConfig, access_token: str) -> dict[str, Any]:
    response = requests.get(
        config.userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
        timeout=config.timeout_seconds,
    )
    response.raise_for_status()
    return response.json()


def normalize_claims(claims: Mapping[str, Any]) -> dict[str, Any]:
    email = claims.get("email") or claims.get("preferred_username")
    name = claims.get("name") or claims.get("given_name") or claims.get("sub")
    return {
        "sub": claims.get("sub"),
        "issuer": claims.get("iss"),
        "subject": claims.get("sub"),
        "email": email,
        "name": name,
        "claims": dict(claims),
    }


def load_json_config(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("Configuration file must contain a JSON object")
    return data

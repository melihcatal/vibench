from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urlencode, urljoin


@dataclass(frozen=True)
class IdentityProviderConfig:
    issuer: str
    client_id: str
    redirect_uri: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    scopes: str = "openid profile email"
    audience: Optional[str] = None


def _clean_base_url(value: str) -> str:
    return value.rstrip("/")


def load_identity_provider_config(prefix: str = "FEDERATED_LOGIN_") -> IdentityProviderConfig:
    issuer = _clean_base_url(os.environ[f"{prefix}ISSUER"])
    client_id = os.environ[f"{prefix}CLIENT_ID"]
    redirect_uri = os.environ[f"{prefix}REDIRECT_URI"]
    authorization_endpoint = os.environ.get(f"{prefix}AUTHORIZATION_ENDPOINT", urljoin(issuer + "/", ".well-known/openid-configuration"))
    token_endpoint = os.environ.get(f"{prefix}TOKEN_ENDPOINT", urljoin(issuer + "/", "oauth/token"))
    userinfo_endpoint = os.environ.get(f"{prefix}USERINFO_ENDPOINT", urljoin(issuer + "/", "userinfo"))
    scopes = os.environ.get(f"{prefix}SCOPES", "openid profile email")
    audience = os.environ.get(f"{prefix}AUDIENCE")
    return IdentityProviderConfig(
        issuer=issuer,
        client_id=client_id,
        redirect_uri=redirect_uri,
        authorization_endpoint=authorization_endpoint,
        token_endpoint=token_endpoint,
        userinfo_endpoint=userinfo_endpoint,
        scopes=scopes,
        audience=audience,
    )


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def generate_code_verifier() -> str:
    return secrets.token_urlsafe(96)


def generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def build_authorization_url(
    config: IdentityProviderConfig,
    state: str,
    code_challenge: Optional[str] = None,
    response_mode: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> str:
    params: Dict[str, str] = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scopes,
        "state": state,
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    if config.audience:
        params["audience"] = config.audience
    if response_mode:
        params["response_mode"] = response_mode
    if extra_params:
        params.update(extra_params)
    return f"{config.authorization_endpoint}?{urlencode(params)}"


def build_token_request_payload(
    config: IdentityProviderConfig,
    code: str,
    code_verifier: Optional[str] = None,
) -> Dict[str, str]:
    payload: Dict[str, str] = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": code,
        "redirect_uri": config.redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    return payload


def normalize_claims(claims: Dict[str, object]) -> Dict[str, object]:
    normalized = dict(claims)
    if "sub" in normalized and "user_id" not in normalized:
        normalized["user_id"] = normalized["sub"]
    if "email_verified" in normalized and isinstance(normalized["email_verified"], str):
        normalized["email_verified"] = normalized["email_verified"].lower() == "true"
    if "name" not in normalized:
        given = normalized.get("given_name")
        family = normalized.get("family_name")
        if given or family:
            normalized["name"] = " ".join(part for part in [given, family] if part)
    return normalized

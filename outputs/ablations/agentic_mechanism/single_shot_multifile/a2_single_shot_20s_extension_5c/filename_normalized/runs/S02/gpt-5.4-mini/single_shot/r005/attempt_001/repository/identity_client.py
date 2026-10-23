import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urlencode

import jwt
import requests


@dataclass(frozen=True)
class IdentityConfig:
    domain: str
    client_id: str
    client_secret: str | None
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    issuer: str


def get_identity_config() -> IdentityConfig:
    domain = os.getenv("AUTH0_DOMAIN", "")
    client_id = os.getenv("AUTH0_CLIENT_ID", "")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    issuer = os.getenv("AUTH0_ISSUER", f"https://{domain}/") if domain else ""
    base = f"https://{domain}" if domain else ""
    return IdentityConfig(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        authorization_endpoint=f"{base}/authorize",
        token_endpoint=f"{base}/oauth/token",
        userinfo_endpoint=f"{base}/userinfo",
        issuer=issuer,
    )


def build_oidc_authorize_url(
    *,
    config: IdentityConfig,
    state: str,
    nonce: str,
    code_challenge: str | None = None,
    code_challenge_method: str | None = None,
    prompt: str | None = None,
    login_hint: str | None = None,
    scope: str | None = None,
) -> str:
    params: dict[str, str] = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": os.getenv("AUTH0_REDIRECT_URI", ""),
        "scope": scope or os.getenv("AUTH0_SCOPE", "openid profile email"),
        "state": state,
        "nonce": nonce,
    }
    if prompt:
        params["prompt"] = prompt
    if login_hint:
        params["login_hint"] = login_hint
    if code_challenge:
        params["code_challenge"] = code_challenge
    if code_challenge_method:
        params["code_challenge_method"] = code_challenge_method
    return f"{config.authorization_endpoint}?{urlencode(params)}"


def normalize_id_token_claims(id_token: str | None, issuer: str) -> dict[str, Any]:
    if not id_token:
        return {}
    try:
        return jwt.decode(id_token, options={"verify_signature": False, "verify_aud": False}, issuer=issuer)
    except Exception:
        return {}


def normalize_profile_claims(payload: Mapping[str, Any]) -> dict[str, Any]:
    name = payload.get("name") or " ".join(
        part for part in [payload.get("given_name"), payload.get("family_name")] if part
    ).strip()
    return {
        "subject": payload.get("sub") or payload.get("user_id") or "",
        "email": payload.get("email") or "",
        "email_verified": bool(payload.get("email_verified", False)),
        "display_name": name or payload.get("nickname") or payload.get("preferred_username") or "",
        "given_name": payload.get("given_name"),
        "family_name": payload.get("family_name"),
        "picture": payload.get("picture"),
        "locale": payload.get("locale"),
        "provider": payload.get("iss") or "Auth0",
        "raw": dict(payload),
    }

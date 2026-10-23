import base64
import hashlib
import os
import secrets
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class LoginRequest:
    scope: str = "openid profile email"
    redirect_uri: Optional[str] = None
    state: Optional[str] = None
    nonce: Optional[str] = None
    response_mode: Optional[str] = None


@dataclass
class PKCELoginRequest:
    redirect_uri: str
    scope: str = "openid profile email"
    state: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    nonce: Optional[str] = None
    response_mode: Optional[str] = None


@dataclass
class CallbackRequest:
    code: str
    redirect_uri: Optional[str] = None
    code_verifier: str = ""


@dataclass
class LoginStartResponse:
    authorization_url: str
    state: str
    code_verifier: str
    code_challenge: str
    provider: str
    client_id: str


@dataclass
class PKCELoginStartResponse(LoginStartResponse):
    pass


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    scope: Optional[str]
    claims: Dict[str, Any]
    provider: str


@dataclass
class ProfileClaims:
    subject: str
    email: Optional[str]
    email_verified: Optional[bool]
    full_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    provider: str
    raw: Dict[str, Any]


def create_pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("utf-8")).digest()).decode("utf-8").rstrip("=")
    return verifier, challenge


def normalize_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(claims)
    if "sub" not in normalized and "subject" in normalized:
        normalized["sub"] = normalized["subject"]
    if "name" not in normalized:
        first = normalized.get("given_name") or ""
        last = normalized.get("family_name") or ""
        merged = (first + " " + last).strip()
        if merged:
            normalized["name"] = merged
    return normalized


def normalize_profile_claims(claims: Dict[str, Any], provider: str) -> ProfileClaims:
    return ProfileClaims(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        provider=provider,
        raw=claims,
    )

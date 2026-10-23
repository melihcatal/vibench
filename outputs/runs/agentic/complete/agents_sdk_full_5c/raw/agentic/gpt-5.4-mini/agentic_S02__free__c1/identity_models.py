from __future__ import annotations

import base64
import hashlib
import re
import secrets
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, Tuple


@dataclass
class AuthRequest:
    provider: str
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    nonce: str
    code_challenge: str
    code_challenge_method: str = "S256"


@dataclass
class CallbackRequest:
    code: str
    redirect_uri: str
    client_id: str
    code_verifier: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    scope: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProfileClaims:
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    issuer: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_pkce_pair() -> Tuple[str, str]:
    verifier = secrets.token_urlsafe(48)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return verifier, challenge


def normalize_token_response(data: Dict[str, Any]) -> TokenResponse:
    return TokenResponse(
        access_token=data.get("access_token"),
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type"),
        expires_in=data.get("expires_in"),
        scope=data.get("scope"),
    )


def normalize_profile_claims(raw: Dict[str, Any]) -> ProfileClaims:
    subject = raw.get("sub") or raw.get("id") or "unknown"
    return ProfileClaims(
        subject=subject,
        email=raw.get("email"),
        email_verified=raw.get("email_verified"),
        name=raw.get("name"),
        given_name=raw.get("given_name"),
        family_name=raw.get("family_name"),
        picture=raw.get("picture"),
        issuer=raw.get("iss"),
    )


def ensure_https_url(url: str) -> str:
    if not re.match(r"^https://", url):
        raise ValueError("redirect_uri must use https")
    return url

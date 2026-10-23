from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class LoginRequest:
    provider: str
    redirect_uri: str
    scope: str


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None


@dataclass
class NormalizedProfile:
    subject: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_claims(claims: Dict[str, Any]) -> NormalizedProfile:
    return NormalizedProfile(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        display_name=claims.get("name") or claims.get("preferred_username"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        raw=claims,
    )


def to_dict(model: Any) -> Dict[str, Any]:
    return asdict(model)

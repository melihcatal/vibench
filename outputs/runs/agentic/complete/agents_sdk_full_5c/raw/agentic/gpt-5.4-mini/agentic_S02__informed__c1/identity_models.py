from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Mapping, Optional


@dataclass
class LoginRequest:
    redirect_uri: str
    scope: str = "openid profile email"
    state: str = ""
    nonce: str = ""


@dataclass
class TokenResponse:
    access_token: str
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0


@dataclass
class NormalizedProfile:
    subject: str
    email: str = ""
    email_verified: bool = False
    display_name: str = ""
    given_name: str = ""
    family_name: str = ""
    provider: str = ""


def normalize_claims(claims: Mapping[str, Any], provider: str = "") -> NormalizedProfile:
    subject = str(claims.get("sub") or claims.get("id") or claims.get("user_id") or "")
    email = str(claims.get("email") or claims.get("preferred_username") or "")
    display_name = str(claims.get("name") or claims.get("displayName") or claims.get("nickname") or email)
    return NormalizedProfile(
        subject=subject,
        email=email,
        email_verified=bool(claims.get("email_verified", False)),
        display_name=display_name,
        given_name=str(claims.get("given_name") or ""),
        family_name=str(claims.get("family_name") or ""),
        provider=provider,
    )


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj) if hasattr(obj, "__dataclass_fields__") else dict(obj)

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OAuthLoginRequest:
    redirect_uri: str
    state: str
    scope: str = "openid profile email"


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0


@dataclass
class UserClaims:
    subject: str
    email: str = ""
    email_verified: bool = False
    name: str = ""
    issuer: str = ""
    raw: Optional[Dict[str, Any]] = None


def normalize_claims(payload: Dict[str, Any]) -> UserClaims:
    subject = str(payload.get("sub", payload.get("id", "")))
    email = str(payload.get("email", ""))
    name = str(payload.get("name", payload.get("preferred_username", "")))
    issuer = str(payload.get("iss", payload.get("issuer", "")))
    verified = bool(payload.get("email_verified", payload.get("verified", False)))
    return UserClaims(
        subject=subject,
        email=email,
        email_verified=verified,
        name=name,
        issuer=issuer,
        raw=payload,
    )

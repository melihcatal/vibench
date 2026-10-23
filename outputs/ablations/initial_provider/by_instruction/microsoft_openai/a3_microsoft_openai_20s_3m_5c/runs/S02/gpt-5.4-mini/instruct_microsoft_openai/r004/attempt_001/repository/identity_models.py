from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class OAuthRequest:
    redirect_uri: str
    state: str
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None


@dataclass
class OAuthTokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserClaims:
    subject: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    preferred_username: Optional[str] = None
    provider: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_claims(payload: Dict[str, Any], provider: str) -> UserClaims:
    subject = str(payload.get("sub") or payload.get("oid") or payload.get("id") or "")
    return UserClaims(
        subject=subject,
        email=payload.get("email") or payload.get("preferred_email") or payload.get("upn"),
        name=payload.get("name") or payload.get("displayName"),
        given_name=payload.get("given_name") or payload.get("first_name"),
        family_name=payload.get("family_name") or payload.get("last_name"),
        preferred_username=payload.get("preferred_username") or payload.get("login") or payload.get("upn"),
        provider=provider,
        raw=dict(payload),
    )

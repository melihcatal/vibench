from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional


def normalize_email(value: Optional[str]) -> Optional[str]:
    return value.strip().lower() if value and value.strip() else None


def normalize_name(parts: Iterable[Optional[str]]) -> Optional[str]:
    cleaned = [p.strip() for p in parts if p and p.strip()]
    return " ".join(cleaned) if cleaned else None


def normalize_profile_claims(claims: Mapping[str, Any]) -> Dict[str, Any]:
    email = normalize_email(claims.get("email") or claims.get("preferred_username"))
    given = claims.get("given_name")
    family = claims.get("family_name")
    name = claims.get("name") or normalize_name([given, family])
    return {
        "sub": claims.get("sub"),
        "email": email,
        "name": name,
        "given_name": given,
        "family_name": family,
        "locale": claims.get("locale"),
        "picture": claims.get("picture"),
        "issuer": claims.get("iss") or claims.get("issuer"),
        "verified_email": bool(claims.get("email_verified")),
    }


@dataclass
class LoginRequest:
    issuer: str
    client_id: str
    redirect_uri: str
    scope: str = "openid profile email"
    state: Optional[str] = None
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    scope: Optional[str] = None


@dataclass
class ProfileClaims:
    subject: Optional[str]
    email: Optional[str]
    display_name: Optional[str]
    raw: Dict[str, Any]

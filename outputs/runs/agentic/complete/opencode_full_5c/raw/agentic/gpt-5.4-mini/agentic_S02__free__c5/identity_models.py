from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass
class LoginRequest:
    client_id: str
    redirect_uri: str
    scope: str = "openid profile email"
    state: str = ""
    nonce: str = ""


@dataclass
class TokenExchangeRequest:
    code: str
    redirect_uri: str
    client_id: str
    client_secret: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class ProfileClaims:
    subject: str
    email: str = ""
    email_verified: bool = False
    given_name: str = ""
    family_name: str = ""
    full_name: str = ""
    issuer: str = ""
    raw: Optional[Dict[str, Any]] = None


def normalize_claims(payload: Mapping[str, Any], issuer: str = "") -> ProfileClaims:
    subject = str(payload.get("sub", payload.get("id", "")))
    email = str(payload.get("email", ""))
    given_name = str(payload.get("given_name", payload.get("first_name", "")))
    family_name = str(payload.get("family_name", payload.get("last_name", "")))
    full_name = str(payload.get("name", "")).strip()
    if not full_name:
        full_name = (given_name + " " + family_name).strip()
    return ProfileClaims(
        subject=subject,
        email=email,
        email_verified=bool(payload.get("email_verified", False)),
        given_name=given_name,
        family_name=family_name,
        full_name=full_name,
        issuer=issuer or str(payload.get("iss", "")),
        raw=dict(payload),
    )

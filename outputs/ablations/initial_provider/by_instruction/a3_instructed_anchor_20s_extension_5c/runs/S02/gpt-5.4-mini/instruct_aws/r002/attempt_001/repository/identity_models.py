from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class OAuthLoginRequest:
    client_id: str
    redirect_uri: str
    scope: str = "openid profile email"
    state: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class NormalizedClaims:
    subject: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    issuer: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_claims(payload: Dict[str, Any]) -> NormalizedClaims:
    return NormalizedClaims(
        subject=str(payload.get("sub", "")),
        email=payload.get("email"),
        name=payload.get("name"),
        given_name=payload.get("given_name"),
        family_name=payload.get("family_name"),
        issuer=payload.get("iss"),
        raw=payload,
    )


def to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)

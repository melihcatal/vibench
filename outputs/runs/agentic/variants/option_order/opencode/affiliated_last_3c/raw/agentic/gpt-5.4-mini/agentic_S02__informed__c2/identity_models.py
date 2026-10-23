from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional


@dataclass
class OAuthConfig:
    issuer: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    scope: str = "openid profile email"


@dataclass
class AuthorizationRequest:
    state: str
    nonce: str
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None


def normalize_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    display_name = (
        claims.get("name")
        or claims.get("preferred_username")
        or claims.get("email")
        or ""
    )
    email = claims.get("email") or claims.get("upn") or claims.get("preferred_username")
    groups = claims.get("groups") or claims.get("roles") or []
    if isinstance(groups, str):
        groups = [groups]
    return {
        "subject": claims.get("sub", ""),
        "display_name": display_name,
        "email": email,
        "email_verified": bool(claims.get("email_verified", False)),
        "issuer": claims.get("iss", ""),
        "tenant": claims.get("tid") or claims.get("tenant") or "",
        "groups": list(groups),
        "raw": claims,
    }


def select_first(values: Iterable[Optional[str]]) -> str:
    for value in values:
        if value:
            return value
    return ""

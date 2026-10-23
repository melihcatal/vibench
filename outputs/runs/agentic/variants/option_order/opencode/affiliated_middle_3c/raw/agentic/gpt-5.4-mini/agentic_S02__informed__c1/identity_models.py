from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LoginRequest:
    redirect_uri: str
    state: str
    scopes: List[str] = field(default_factory=list)
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "subject": claims.get("sub") or claims.get("id") or claims.get("user_id"),
        "email": claims.get("email") or claims.get("preferred_username"),
        "name": claims.get("name")
        or claims.get("given_name")
        or claims.get("nickname"),
        "picture": claims.get("picture") or claims.get("avatar_url"),
        "provider": claims.get("iss") or claims.get("provider"),
        "raw": claims,
    }

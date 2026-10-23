from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OAuthLoginRequest:
    client_id: str
    redirect_uri: str
    scope: str
    state: str
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    raw: Dict[str, Any]


def normalize_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "sub": claims.get("sub") or claims.get("user_id") or claims.get("id"),
        "email": (claims.get("email") or "").lower() or None,
        "name": claims.get("name") or claims.get("preferred_username") or claims.get("nickname"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture") or claims.get("avatar_url"),
        "locale": claims.get("locale"),
        "raw": claims,
    }

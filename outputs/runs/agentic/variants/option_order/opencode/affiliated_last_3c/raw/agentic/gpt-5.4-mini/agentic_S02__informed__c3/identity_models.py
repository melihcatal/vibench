from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OAuthLoginRequest:
    state: str
    redirect_uri: str
    scope: str = "openid profile email"


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "subject": claims.get("sub") or claims.get("user_id") or claims.get("id"),
        "email": claims.get("email"),
        "email_verified": bool(claims.get("email_verified", False)),
        "name": claims.get("name")
        or claims.get("preferred_username")
        or claims.get("nickname"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture"),
        "raw": claims,
    }

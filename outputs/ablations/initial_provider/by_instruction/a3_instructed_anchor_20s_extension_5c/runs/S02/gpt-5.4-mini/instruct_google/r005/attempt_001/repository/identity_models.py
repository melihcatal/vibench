from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OAuthClientConfig:
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    issuer: str
    scope: str = "openid email profile"


@dataclass
class AuthorizationResult:
    authorization_url: str
    state: str
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: Optional[str]
    expires_in: Optional[int]
    raw: Dict[str, Any]


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "subject": claims.get("sub") or claims.get("id") or claims.get("user_id"),
        "email": claims.get("email"),
        "email_verified": bool(claims.get("email_verified")),
        "name": claims.get("name") or claims.get("full_name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture") or claims.get("avatar_url"),
        "locale": claims.get("locale"),
        "raw": claims,
    }

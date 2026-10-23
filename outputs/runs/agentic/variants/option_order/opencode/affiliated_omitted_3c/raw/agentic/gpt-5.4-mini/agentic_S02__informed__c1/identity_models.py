from dataclasses import dataclass
from typing import Any, Dict, Optional


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
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None
    nonce: Optional[str] = None
    redirect_uri: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


def normalize_claims(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "sub": raw.get("sub") or raw.get("user_id") or raw.get("id"),
        "email": raw.get("email") or raw.get("preferred_email"),
        "name": raw.get("name") or raw.get("preferred_username") or raw.get("nickname"),
        "given_name": raw.get("given_name"),
        "family_name": raw.get("family_name"),
        "locale": raw.get("locale"),
        "picture": raw.get("picture") or raw.get("avatar_url"),
        "raw": raw,
    }

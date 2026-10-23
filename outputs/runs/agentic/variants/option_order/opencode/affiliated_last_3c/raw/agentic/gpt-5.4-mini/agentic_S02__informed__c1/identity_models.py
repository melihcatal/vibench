from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OAuthRequest:
    redirect_uri: str
    state: str
    scope: str = "openid profile email"
    response_type: str = "code"
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_claims(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "subject": payload.get("sub") or payload.get("user_id") or payload.get("id"),
        "email": payload.get("email"),
        "email_verified": bool(payload.get("email_verified", False)),
        "name": payload.get("name") or payload.get("preferred_username"),
        "given_name": payload.get("given_name"),
        "family_name": payload.get("family_name"),
        "issuer": payload.get("iss"),
        "claims": payload,
    }

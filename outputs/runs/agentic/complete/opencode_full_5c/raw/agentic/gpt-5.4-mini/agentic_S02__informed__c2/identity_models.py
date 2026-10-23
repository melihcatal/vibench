from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OAuthRequest:
    redirect_uri: str
    scope: str
    state: str
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]


def normalize_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "subject": claims.get("sub") or claims.get("oid") or claims.get("user_id"),
        "email": claims.get("email") or claims.get("preferred_username"),
        "name": claims.get("name")
        or claims.get("given_name")
        or claims.get("nickname"),
        "issuer": claims.get("iss"),
        "tenant": claims.get("tid") or claims.get("tenant_id"),
        "raw": claims,
    }

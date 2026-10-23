from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class OAuthLoginRequest:
    redirect_uri: str
    scope: str = "openid profile email"
    state: Optional[str] = None


@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class FederatedProfile:
    subject: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    provider: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_claims(claims: Dict[str, Any], provider: str) -> FederatedProfile:
    subject = str(claims.get("sub") or claims.get("oid") or claims.get("id") or "")
    email = claims.get("email") or claims.get("preferred_username")
    display_name = claims.get("name") or claims.get("given_name")
    return FederatedProfile(subject=subject, email=email, display_name=display_name, provider=provider, raw=claims)

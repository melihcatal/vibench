from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OAuthConfig:
    authority: str = "https://login.microsoftonline.com/common"
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = ""
    scopes: List[str] = field(default_factory=lambda: ["openid", "profile", "email", "offline_access"])
    tenant_id: str = "common"


@dataclass
class TokenResponse:
    access_token: str
    id_token: str = ""
    refresh_token: str = ""
    expires_in: int = 0
    token_type: str = "Bearer"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedProfile:
    subject: str
    display_name: str = ""
    email: str = ""
    provider: str = "microsoft"
    claims: Dict[str, Any] = field(default_factory=dict)


def normalize_claims(claims: Dict[str, Any]) -> NormalizedProfile:
    subject = str(claims.get("sub") or claims.get("oid") or claims.get("id") or "")
    display_name = str(claims.get("name") or claims.get("preferred_username") or claims.get("given_name") or "")
    email = str(claims.get("email") or claims.get("preferred_username") or claims.get("upn") or "")
    return NormalizedProfile(subject=subject, display_name=display_name, email=email, claims=claims)

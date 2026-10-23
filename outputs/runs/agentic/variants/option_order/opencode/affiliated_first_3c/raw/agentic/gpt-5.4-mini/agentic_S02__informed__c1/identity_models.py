from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class OAuthClientConfig:
    issuer: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    scopes: tuple[str, ...] = ("openid", "profile", "email")
    tenant_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuthorizationRequest:
    state: str
    nonce: str
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    redirect_uri: Optional[str] = None
    scope: str = "openid profile email"


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(claims)
    if "sub" in normalized and "user_id" not in normalized:
        normalized["user_id"] = normalized["sub"]
    if "preferred_username" in normalized and "username" not in normalized:
        normalized["username"] = normalized["preferred_username"]
    if "email" in normalized:
        normalized["email"] = str(normalized["email"]).lower()
    return normalized

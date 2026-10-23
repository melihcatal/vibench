from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class OAuthConfig:
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    audience: Optional[str]
    scopes: list[str]


@dataclass(frozen=True)
class AuthorizationRequest:
    authorization_url: str
    state: str
    code_verifier: Optional[str] = None


@dataclass(frozen=True)
class TokenResponse:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    scope: Optional[str]


@dataclass(frozen=True)
class FederatedProfile:
    provider: str
    subject: str
    email: Optional[str]
    email_verified: Optional[bool]
    display_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    raw_claims: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AuditRecord:
    event_type: str
    provider: str
    subject: Optional[str]
    outcome: str
    metadata: Dict[str, Any]

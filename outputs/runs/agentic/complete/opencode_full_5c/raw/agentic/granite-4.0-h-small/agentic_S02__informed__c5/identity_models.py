from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class AuthRequest:
    """Model for the initial authentication request.",
    redirect_uri: str
    scopes: list[str]
    code_challenge_method: str = "S256"

@dataclass(frozen=True)
class TokenResponse:
    """Model for the token response returned by the provider.",
    access_token: str
    id_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None

@dataclass(frozen=True)
class UserInfo:
    """Model for the normalized user profile claims.",
    subject: str
    email: str | None = None
    email_verified: bool | None = None
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    locale: str | None = None
    picture: str | None = None
    # Additional claims can be added as needed

@dataclass(frozen=True)
class AuditEvent:
    """Base model for audit events.",
    event_name: str
    payload: Dict[str, Any]

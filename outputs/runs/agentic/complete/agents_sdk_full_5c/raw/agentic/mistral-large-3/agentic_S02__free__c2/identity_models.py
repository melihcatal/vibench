from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str]
    expires_in: int


@dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    picture: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class LoginAuditRecord:
    user_id: str
    provider: str
    timestamp: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    claims: Optional[dict] = None


@dataclass
class ModerationResult:
    is_flagged: bool
    flags: list[str]
    sanitized_text: Optional[str] = None
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
    name: Optional[str]
    email: Optional[str]
    email_verified: bool
    picture: Optional[str]
    locale: Optional[str]
    provider: str


@dataclass
class LoginAuditRecord:
    user_id: str
    provider: str
    timestamp: str
    ip_address: str
    user_agent: str
    claims: dict
    status: str
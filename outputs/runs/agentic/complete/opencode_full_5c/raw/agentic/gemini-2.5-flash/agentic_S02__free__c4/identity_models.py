from dataclasses import dataclass


@dataclass
class UserProfileClaims:
    sub: str  # Subject identifier
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    email: str | None = None
    email_verified: bool | None = None
    picture: str | None = None
    locale: str | None = None


@dataclass
class AuthTokens:
    access_token: str
    token_type: str
    expires_in: int
    id_token: str | None = None
    refresh_token: str | None = None


@dataclass
class AuditRecord:
    event_id: str
    timestamp: str
    user_id: str
    event_type: str
    details: dict

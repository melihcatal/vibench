import dataclasses
from typing import Optional


@dataclasses.dataclass
class UserRegistrationRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class UserLoginRequest:
    email: str
    password: str
    audience: str
    scope: str = "openid profile email"
    grant_type: str = "password"
    client_id: str


@dataclasses.dataclass
class TokenRefreshRequest:
    refresh_token: str
    client_id: str
    grant_type: str = "refresh_token"


@dataclasses.dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"
    client_id: str


@dataclasses.dataclass
class AuthTokens:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


@dataclasses.dataclass
class UserProfile:
    user_id: str
    email: str
    nickname: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    updated_at: Optional[str] = None


@dataclasses.dataclass
class ModerationResult:
    blocked: bool
    reason: Optional[str] = None


@dataclasses.dataclass
class OnboardingSummary:
    summary_text: str


@dataclasses.dataclass
class ProfileNote:
    user_id: str
    note_text: str
    timestamp: str

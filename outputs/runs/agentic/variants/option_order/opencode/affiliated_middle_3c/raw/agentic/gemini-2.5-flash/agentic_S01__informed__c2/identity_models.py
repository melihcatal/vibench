import dataclasses
from typing import Optional


@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class RegisterUserResponse:
    user_id: str
    email: str
    email_verified: bool


@dataclasses.dataclass
class LoginUserRequest:
    email: str
    password: str
    audience: str
    scope: str = "openid profile email offline_access"
    grant_type: str = "password"


@dataclasses.dataclass
class LoginUserResponse:
    access_token: str
    refresh_token: str
    id_token: str
    token_type: str
    expires_in: int


@dataclasses.dataclass
class RefreshTokenRequest:
    refresh_token: str
    scope: str = "openid profile email offline_access"
    grant_type: str = "refresh_token"


@dataclasses.dataclass
class RefreshTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    token_type: str
    expires_in: int


@dataclasses.dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str


@dataclasses.dataclass
class ModerationRequest:
    text: str


@dataclasses.dataclass
class ModerationResponse:
    is_toxic: bool
    score: float


@dataclasses.dataclass
class SummaryRequest:
    text: str


@dataclasses.dataclass
class SummaryResponse:
    summary: str


@dataclasses.dataclass
class ProfileNote:
    user_id: str
    note_id: str
    content: str
    timestamp: str
    metadata: dict

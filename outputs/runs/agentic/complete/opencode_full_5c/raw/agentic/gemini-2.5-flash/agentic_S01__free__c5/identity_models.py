from dataclasses import dataclass
from typing import Optional


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None


@dataclass
class RegisterUserResponse:
    uid: str
    email: str
    display_name: Optional[str] = None


@dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str


@dataclass
class EmailPasswordLoginResponse:
    id_token: str
    refresh_token: str
    expires_in: str


@dataclass
class RefreshSessionRequest:
    refresh_token: str


@dataclass
class RefreshSessionResponse:
    id_token: str
    expires_in: str


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class PasswordResetResponse:
    message: str


@dataclass
class UserProfile:
    uid: str
    display_name: str
    bio: str
    locale: str


@dataclass
class OnboardingSummary:
    user_id: str
    summary_text: str


@dataclass
class ProfileNote:
    user_id: str
    note_id: str
    content: str
    timestamp: str

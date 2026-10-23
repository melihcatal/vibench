from dataclasses import dataclass
from typing import Optional


@dataclass
class UserRegistrationRequest:
    email: str
    password: str


@dataclass
class UserRegistrationResponse:
    uid: str


@dataclass
class UserLoginRequest:
    email: str
    password: str


@dataclass
class UserLoginResponse:
    custom_token: str


@dataclass
class TokenRefreshRequest:
    uid: str


@dataclass
class TokenRefreshResponse:
    custom_token: str


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class PasswordResetResponse:
    reset_link: str


@dataclass
class OnboardingNote:
    user_id: str
    note: str
    timestamp: str

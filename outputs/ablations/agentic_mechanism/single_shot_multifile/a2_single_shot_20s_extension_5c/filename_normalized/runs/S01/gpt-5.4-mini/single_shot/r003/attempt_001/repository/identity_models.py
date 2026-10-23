from dataclasses import dataclass
from typing import Any, Dict, Optional


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en").replace("_", "-").lower()


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    locale: str = "en"

    def __post_init__(self) -> None:
        self.email = _normalize_email(self.email)
        self.locale = _normalize_locale(self.locale)


@dataclass
class LoginRequest:
    email: str
    password: str

    def __post_init__(self) -> None:
        self.email = _normalize_email(self.email)


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class PasswordResetRequest:
    email: str

    def __post_init__(self) -> None:
        self.email = _normalize_email(self.email)


@dataclass
class AuthResult:
    email: str
    access_token: str
    refresh_token: str
    id_token: str
    raw: Dict[str, Any]


@dataclass
class LoginResponse(AuthResult):
    pass


@dataclass
class RegisterUserResponse(AuthResult):
    pass


@dataclass
class RefreshResponse:
    access_token: str
    refresh_token: str
    id_token: str
    raw: Dict[str, Any]


@dataclass
class PasswordResetResponse:
    requested: bool
    email: str

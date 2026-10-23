from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


@dataclass(frozen=True)
class RegisterUserRequest:
    email: str
    password: str
    locale: Optional[str] = None
    display_name: Optional[str] = None


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str


@dataclass(frozen=True)
class RefreshRequest:
    refresh_token: str


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str


@dataclass(frozen=True)
class TextRequest:
    text: str
    locale: Optional[str] = None


def to_payload(obj: Any) -> Dict[str, Any]:
    return {k: v for k, v in asdict(obj).items() if v is not None}

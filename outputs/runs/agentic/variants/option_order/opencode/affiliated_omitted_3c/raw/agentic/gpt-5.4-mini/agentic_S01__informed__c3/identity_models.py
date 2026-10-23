from dataclasses import dataclass
from typing import Any, Dict, Optional


def _clean_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def normalize_email(email: Any) -> str:
    value = _clean_string(email)
    if not value or "@" not in value:
        raise ValueError("valid email required")
    return value.lower()


def normalize_password(password: Any) -> str:
    value = _clean_string(password)
    if not value:
        raise ValueError("password required")
    return value


def normalize_locale(locale: Any, default: str = "en-US") -> str:
    value = _clean_string(locale)
    return value or default


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    locale: str = "en-US"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email": normalize_email(self.email),
            "password": normalize_password(self.password),
            "locale": normalize_locale(self.locale),
        }


@dataclass
class LoginRequest:
    email: str
    password: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email": normalize_email(self.email),
            "password": normalize_password(self.password),
        }


@dataclass
class RefreshRequest:
    refresh_token: str

    def to_dict(self) -> Dict[str, Any]:
        token = _clean_string(self.refresh_token)
        if not token:
            raise ValueError("refresh token required")
        return {"refresh_token": token}


@dataclass
class PasswordResetRequest:
    email: str

    def to_dict(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email)}

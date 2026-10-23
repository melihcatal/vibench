from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_password(value: str) -> str:
    return value.strip()


def normalize_token(value: str) -> str:
    return value.strip()


def normalize_locale(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip().replace("_", "-")
    return cleaned or None


@dataclass
class RegisterRequest:
    email: str
    password: str
    locale: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"email": self.email, "password": self.password}
        if self.locale:
            payload["locale"] = self.locale
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload


@dataclass
class LoginRequest:
    email: str
    password: str

    def to_payload(self) -> Dict[str, Any]:
        return {"email": self.email, "password": self.password}


@dataclass
class RefreshRequest:
    refresh_token: str

    def to_payload(self) -> Dict[str, Any]:
        return {"refresh_token": self.refresh_token}


@dataclass
class PasswordResetRequest:
    email: str

    def to_payload(self) -> Dict[str, Any]:
        return {"email": self.email}

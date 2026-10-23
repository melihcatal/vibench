from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


@dataclass(frozen=True)
class RegistrationRequest:
    email: str
    password: str
    name: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"email": self.email, "password": self.password}
        if self.name:
            payload["user_metadata"] = {"name": self.name}
        return payload


@dataclass(frozen=True)
class RegistrationResponse:
    user_id: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "RegistrationResponse":
        return cls(
            user_id=payload.get("_id") or payload.get("user_id") or payload.get("id"),
            email=payload.get("email"),
            status=payload.get("status") or payload.get("message"),
        )


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str

    def to_payload(self) -> Dict[str, Any]:
        return {"username": self.email, "password": self.password}


@dataclass(frozen=True)
class LoginResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "LoginResponse":
        return cls(
            access_token=payload.get("access_token"),
            id_token=payload.get("id_token"),
            refresh_token=payload.get("refresh_token"),
            token_type=payload.get("token_type"),
            expires_in=payload.get("expires_in"),
        )


@dataclass(frozen=True)
class RefreshRequest:
    refresh_token: str

    def to_payload(self) -> Dict[str, Any]:
        return {"refresh_token": self.refresh_token}


@dataclass(frozen=True)
class RefreshResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "RefreshResponse":
        return cls(
            access_token=payload.get("access_token"),
            id_token=payload.get("id_token"),
            refresh_token=payload.get("refresh_token"),
            token_type=payload.get("token_type"),
            expires_in=payload.get("expires_in"),
        )


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str

    def to_payload(self) -> Dict[str, Any]:
        return {"email": self.email}


@dataclass(frozen=True)
class PasswordResetResponse:
    message: Optional[str] = None

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "PasswordResetResponse":
        if isinstance(payload, dict):
            return cls(message=payload.get("message") or payload.get("status"))
        return cls(message=str(payload))

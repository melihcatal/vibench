from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


@dataclass(frozen=True)
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"email": normalize_email(self.email), "password": self.password, "returnSecureToken": True}
        if self.display_name:
            payload["displayName"] = self.display_name.strip()
        return payload


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str

    def to_payload(self) -> Dict[str, Any]:
        return {"email": normalize_email(self.email), "password": self.password, "returnSecureToken": True}


@dataclass(frozen=True)
class RefreshRequest:
    refresh_token: str

    def to_payload(self) -> Dict[str, Any]:
        return {"grant_type": "refresh_token", "refresh_token": self.refresh_token}


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str

    def to_payload(self) -> Dict[str, Any]:
        return {"requestType": "PASSWORD_RESET", "email": normalize_email(self.email)}


def extract_tokens(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id_token": data.get("idToken") or data.get("id_token"),
        "refresh_token": data.get("refreshToken") or data.get("refresh_token"),
        "expires_in": data.get("expiresIn") or data.get("expires_in"),
        "local_id": data.get("localId") or data.get("local_id"),
        "email": data.get("email"),
    }

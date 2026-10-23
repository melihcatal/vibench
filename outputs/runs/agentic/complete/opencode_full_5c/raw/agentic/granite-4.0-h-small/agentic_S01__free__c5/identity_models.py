from __future__ import annotations
from typing import Any, Dict, Optional

# ---------------------------------------------------------------------------
# Shared DTO models for email/password account lifecycle
# ---------------------------------------------------------------------------


class RegisterRequest:
    def __init__(
        self,
        email: str,
        password: str,
        locale: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.email = email
        self.password = password
        self.locale = locale
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "password": self.password,
            "locale": self.locale,
            "metadata": self.metadata,
        }


class RegisterResponse:
    def __init__(
        self,
        user_id: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
    ):
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RegisterResponse:
        return cls(
            user_id=data["user_id"],
            access_token=data.get("access_token"),
            refresh_token=data.get("refresh_token"),
        )


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------


class LoginRequest:
    def __init__(self, email: str, password: str, device_info: Optional[str] = None):
        self.email = email
        self.password = password
        self.device_info = device_info

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "password": self.password,
            "device_info": self.device_info,
        }


class LoginResponse:
    def __init__(self, access_token: str, refresh_token: Optional[str] = None):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> LoginResponse:
        return cls(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
        )


# ---------------------------------------------------------------------------
# Refresh
# ---------------------------------------------------------------------------


class RefreshRequest:
    def __init__(self, refresh_token: str, **extra):
        self.refresh_token = refresh_token
        self.extra = extra  # may contain scopes, device hints, etc.

    def to_dict(self) -> Dict[str, Any]:
        payload = {"refresh_token": self.refresh_token}
        payload.update(self.extra)
        return payload


class RefreshResponse:
    def __init__(self, access_token: str):
        self.access_token = access_token

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RefreshResponse:
        return cls(access_token=data["access_token"])


# ---------------------------------------------------------------------------
# Reset password
# ---------------------------------------------------------------------------


class ResetRequest:
    def __init__(self, email: str, **extra):
        self.email = email
        self.extra = extra  # e.g., redirect_uri, locale

    def to_dict(self) -> Dict[str, Any]:
        payload = {"email": self.email}
        payload.update(self.extra)
        return payload


class ResetResponse:
    def __init__(
        self, reset_url: Optional[str] = None, reset_token: Optional[str] = None
    ):
        self.reset_url = reset_url
        self.reset_token = reset_token

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ResetResponse:
        return cls(
            reset_url=data.get("reset_url"),
            reset_token=data.get("reset_token"),
        )

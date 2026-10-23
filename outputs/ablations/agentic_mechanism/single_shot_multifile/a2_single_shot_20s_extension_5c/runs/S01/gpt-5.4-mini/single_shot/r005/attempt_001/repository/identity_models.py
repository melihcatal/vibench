from dataclasses import dataclass
from typing import Any


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    locale: str | None = None
    display_name: str | None = None

    def to_payload(self) -> dict:
        payload = {"email": self.email, "password": self.password, "returnSecureToken": True}
        if self.locale:
            payload["locale"] = self.locale
        if self.display_name:
            payload["displayName"] = self.display_name
        return payload


@dataclass
class LoginRequest:
    email: str
    password: str

    def to_payload(self) -> dict:
        return {"email": self.email, "password": self.password, "returnSecureToken": True}


@dataclass
class RefreshSessionRequest:
    refresh_token: str

    def to_payload(self) -> dict:
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }


@dataclass
class PasswordResetRequest:
    email: str
    locale: str | None = None

    def to_payload(self) -> dict:
        payload = {"requestType": "PASSWORD_RESET", "email": self.email}
        if self.locale:
            payload["locale"] = self.locale
        return payload


@dataclass
class RegisterUserResponse:
    user_id: str | None
    email: str | None
    id_token: str | None
    refresh_token: str | None
    expires_in: int | None

    @classmethod
    def from_provider(cls, data: dict[str, Any]) -> "RegisterUserResponse":
        return cls(
            user_id=data.get("localId"),
            email=data.get("email"),
            id_token=data.get("idToken"),
            refresh_token=data.get("refreshToken"),
            expires_in=_as_int(data.get("expiresIn")),
        )

    def to_dict(self) -> dict:
        return self.__dict__


@dataclass
class LoginResponse:
    user_id: str | None
    email: str | None
    id_token: str | None
    refresh_token: str | None
    expires_in: int | None

    @classmethod
    def from_provider(cls, data: dict[str, Any]) -> "LoginResponse":
        return cls(
            user_id=data.get("localId"),
            email=data.get("email"),
            id_token=data.get("idToken"),
            refresh_token=data.get("refreshToken"),
            expires_in=_as_int(data.get("expiresIn")),
        )

    def to_dict(self) -> dict:
        return self.__dict__


@dataclass
class RefreshSessionResponse:
    access_token: str | None
    refresh_token: str | None
    expires_in: int | None
    user_id: str | None
    token_type: str | None

    @classmethod
    def from_provider(cls, data: dict[str, Any]) -> "RefreshSessionResponse":
        return cls(
            access_token=data.get("access_token") or data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            expires_in=_as_int(data.get("expires_in")),
            user_id=data.get("user_id") or data.get("localId"),
            token_type=data.get("token_type"),
        )

    def to_dict(self) -> dict:
        return self.__dict__


@dataclass
class PasswordResetResponse:
    email: str | None
    oob_code: str | None

    @classmethod
    def from_provider(cls, data: dict[str, Any]) -> "PasswordResetResponse":
        return cls(email=data.get("email"), oob_code=data.get("oobCode"))

    def to_dict(self) -> dict:
        return self.__dict__


def _as_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except Exception:
        return None

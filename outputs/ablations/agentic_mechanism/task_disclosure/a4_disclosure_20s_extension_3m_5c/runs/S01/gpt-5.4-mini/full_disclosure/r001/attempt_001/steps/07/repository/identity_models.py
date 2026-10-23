from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


def _pick(mapping: Mapping[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in mapping and mapping[name] is not None:
            return mapping[name]
    return default


def _str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _normalize_email(email: Any) -> str:
    return _str(email).strip().lower()


def _normalize_locale(locale: Any) -> str:
    value = _str(locale).strip().replace("_", "-")
    return value.lower()


@dataclass(frozen=True)
class EmailPasswordCredentials:
    email: str
    password: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "EmailPasswordCredentials":
        return cls(
            email=_normalize_email(_pick(data, "email", "username")),
            password=_str(_pick(data, "password", "passphrase")),
        )


@dataclass(frozen=True)
class RegisterUserRequest:
    email: str
    password: str
    locale: str = ""
    display_name: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "RegisterUserRequest":
        return cls(
            email=_normalize_email(_pick(data, "email")),
            password=_str(_pick(data, "password")),
            locale=_normalize_locale(_pick(data, "locale")),
            display_name=_str(_pick(data, "display_name", "name")),
            metadata=dict(_pick(data, "metadata", default={}) or {}),
        )


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "LoginRequest":
        return cls(
            email=_normalize_email(_pick(data, "email", "username")),
            password=_str(_pick(data, "password")),
        )


@dataclass(frozen=True)
class RefreshSessionRequest:
    refresh_token: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "RefreshSessionRequest":
        return cls(refresh_token=_str(_pick(data, "refresh_token", "token")))


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    locale: str = ""

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "PasswordResetRequest":
        return cls(
            email=_normalize_email(_pick(data, "email")),
            locale=_normalize_locale(_pick(data, "locale")),
        )


@dataclass(frozen=True)
class TokenSet:
    access_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    id_token: str = ""

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "TokenSet":
        return cls(
            access_token=_str(_pick(data, "access_token", "accessToken", "token")),
            refresh_token=_str(_pick(data, "refresh_token", "refreshToken")),
            token_type=_str(_pick(data, "token_type", "tokenType", default="Bearer")),
            expires_in=_pick(data, "expires_in", "expiresIn"),
            id_token=_str(_pick(data, "id_token", "idToken")),
        )


@dataclass(frozen=True)
class UserProfile:
    user_id: str = ""
    email: str = ""
    display_name: str = ""
    locale: str = ""
    is_active: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "UserProfile":
        return cls(
            user_id=_str(_pick(data, "user_id", "id", "sub")),
            email=_normalize_email(_pick(data, "email")),
            display_name=_str(_pick(data, "display_name", "name")),
            locale=_normalize_locale(_pick(data, "locale")),
            is_active=bool(_pick(data, "is_active", "active", default=False)),
            metadata=dict(_pick(data, "metadata", default={}) or {}),
        )


@dataclass(frozen=True)
class AuthResponse:
    user: UserProfile = field(default_factory=UserProfile)
    tokens: TokenSet = field(default_factory=TokenSet)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AuthResponse":
        return cls(
            user=UserProfile.from_mapping(_pick(data, "user", "profile", default={}) or {}),
            tokens=TokenSet.from_mapping(_pick(data, "tokens", default=data) or {}),
        )


@dataclass(frozen=True)
class PasswordResetResponse:
    email: str = ""
    delivery_channel: str = ""
    status: str = ""

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "PasswordResetResponse":
        return cls(
            email=_normalize_email(_pick(data, "email")),
            delivery_channel=_str(_pick(data, "delivery_channel", "channel")),
            status=_str(_pick(data, "status", default="requested")),
        )


def normalize_email_password_request(data: Mapping[str, Any]) -> EmailPasswordCredentials:
    return EmailPasswordCredentials.from_mapping(data)


def normalize_register_user_request(data: Mapping[str, Any]) -> RegisterUserRequest:
    return RegisterUserRequest.from_mapping(data)


def normalize_login_request(data: Mapping[str, Any]) -> LoginRequest:
    return LoginRequest.from_mapping(data)


def normalize_refresh_session_request(data: Mapping[str, Any]) -> RefreshSessionRequest:
    return RefreshSessionRequest.from_mapping(data)


def normalize_password_reset_request(data: Mapping[str, Any]) -> PasswordResetRequest:
    return PasswordResetRequest.from_mapping(data)


def normalize_auth_response(data: Mapping[str, Any]) -> AuthResponse:
    return AuthResponse.from_mapping(data)


def normalize_password_reset_response(data: Mapping[str, Any]) -> PasswordResetResponse:
    return PasswordResetResponse.from_mapping(data)

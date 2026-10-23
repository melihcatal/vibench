from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional


def _get(data: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data:
            return data[key]
    return None


def _str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        s = value.strip()
        return s if s else None
    return str(value)


def _bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true", "1", "yes", "y", "on"}:
            return True
        if v in {"false", "0", "no", "n", "off"}:
            return False
    return None


def _int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


@dataclass(frozen=True)
class EmailPasswordRegistrationRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"email": self.email, "password": self.password}
        if self.display_name is not None:
            payload["display_name"] = self.display_name
        return payload


@dataclass(frozen=True)
class EmailPasswordLoginRequest:
    email: str
    password: str

    def to_payload(self) -> dict[str, Any]:
        return {"email": self.email, "password": self.password}


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str

    def to_payload(self) -> dict[str, Any]:
        return {"email": self.email}


@dataclass(frozen=True)
class RefreshSessionRequest:
    refresh_token: str

    def to_payload(self) -> dict[str, Any]:
        return {"refresh_token": self.refresh_token}


@dataclass(frozen=True)
class IdentityTokens:
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    id_token: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "IdentityTokens":
        return cls(
            access_token=_str(_get(data, "access_token", "accessToken", "token")),
            refresh_token=_str(_get(data, "refresh_token", "refreshToken")),
            token_type=_str(_get(data, "token_type", "tokenType")),
            expires_in=_int(_get(data, "expires_in", "expiresIn")),
            id_token=_str(_get(data, "id_token", "idToken")),
        )

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.access_token is not None:
            payload["access_token"] = self.access_token
        if self.refresh_token is not None:
            payload["refresh_token"] = self.refresh_token
        if self.token_type is not None:
            payload["token_type"] = self.token_type
        if self.expires_in is not None:
            payload["expires_in"] = self.expires_in
        if self.id_token is not None:
            payload["id_token"] = self.id_token
        return payload


@dataclass(frozen=True)
class IdentityUser:
    user_id: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    locale: Optional[str] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "IdentityUser":
        return cls(
            user_id=_str(_get(data, "user_id", "userId", "id", "sub")),
            email=_str(_get(data, "email", "emailAddress")),
            display_name=_str(_get(data, "display_name", "displayName", "name")),
            locale=_str(_get(data, "locale", "language")),
            is_verified=_bool(_get(data, "is_verified", "isVerified", "email_verified", "emailVerified")),
            is_active=_bool(_get(data, "is_active", "isActive", "active")),
        )

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.user_id is not None:
            payload["user_id"] = self.user_id
        if self.email is not None:
            payload["email"] = self.email
        if self.display_name is not None:
            payload["display_name"] = self.display_name
        if self.locale is not None:
            payload["locale"] = self.locale
        if self.is_verified is not None:
            payload["is_verified"] = self.is_verified
        if self.is_active is not None:
            payload["is_active"] = self.is_active
        return payload


@dataclass(frozen=True)
class IdentityResponse:
    user: Optional[IdentityUser] = None
    tokens: Optional[IdentityTokens] = None
    message: Optional[str] = None
    status: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "IdentityResponse":
        user_data = _get(data, "user", "account", "profile")
        token_data = _get(data, "tokens", "session", "auth")
        return cls(
            user=IdentityUser.from_mapping(user_data) if isinstance(user_data, Mapping) else None,
            tokens=IdentityTokens.from_mapping(token_data) if isinstance(token_data, Mapping) else None,
            message=_str(_get(data, "message", "detail", "error_description")),
            status=_str(_get(data, "status", "state")),
        )

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.user is not None:
            payload["user"] = self.user.as_dict()
        if self.tokens is not None:
            payload["tokens"] = self.tokens.as_dict()
        if self.message is not None:
            payload["message"] = self.message
        if self.status is not None:
            payload["status"] = self.status
        return payload


def normalize_email(value: Any) -> Optional[str]:
    email = _str(value)
    if email is None:
        return None
    return email.lower()


def normalize_locale(value: Any) -> Optional[str]:
    locale = _str(value)
    if locale is None:
        return None
    return locale.replace("_", "-").lower()


def normalize_display_name(value: Any) -> Optional[str]:
    return _str(value)


def normalize_identity_user(data: Mapping[str, Any]) -> IdentityUser:
    user = IdentityUser.from_mapping(data)
    return IdentityUser(
        user_id=user.user_id,
        email=normalize_email(user.email),
        display_name=normalize_display_name(user.display_name),
        locale=normalize_locale(user.locale),
        is_verified=user.is_verified,
        is_active=user.is_active,
    )


def normalize_identity_response(data: Mapping[str, Any]) -> IdentityResponse:
    response = IdentityResponse.from_mapping(data)
    user = normalize_identity_user(response.user.as_dict()) if response.user is not None else None
    return IdentityResponse(user=user, tokens=response.tokens, message=response.message, status=response.status)

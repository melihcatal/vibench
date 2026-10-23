from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Mapping, Optional


def _normalize_email(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value.lower() if value else None


def _normalize_locale(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip().replace("_", "-")
    return value.lower() if value else None


def _normalize_string(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def _normalize_bool(value: Any) -> Optional[bool]:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true", "1", "yes", "y", "on"}:
            return True
        if v in {"false", "0", "no", "n", "off"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None


def _normalize_mapping(data: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    return dict(data or {})


@dataclass(frozen=True)
class EmailPasswordRegisterRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    locale: Optional[str] = None

    def normalized(self) -> "EmailPasswordRegisterRequest":
        return EmailPasswordRegisterRequest(
            email=_normalize_email(self.email) or self.email,
            password=self.password,
            display_name=_normalize_string(self.display_name),
            locale=_normalize_locale(self.locale),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EmailPasswordLoginRequest:
    email: str
    password: str

    def normalized(self) -> "EmailPasswordLoginRequest":
        return EmailPasswordLoginRequest(
            email=_normalize_email(self.email) or self.email,
            password=self.password,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    locale: Optional[str] = None

    def normalized(self) -> "PasswordResetRequest":
        return PasswordResetRequest(
            email=_normalize_email(self.email) or self.email,
            locale=_normalize_locale(self.locale),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RefreshSessionRequest:
    refresh_token: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AuthTokens:
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AuthTokens":
        return cls(
            access_token=str(data.get("access_token") or data.get("accessToken") or ""),
            refresh_token=data.get("refresh_token") or data.get("refreshToken"),
            token_type=str(data.get("token_type") or data.get("tokenType") or "Bearer"),
            expires_in=data.get("expires_in") or data.get("expiresIn"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EmailPasswordUserProfile:
    user_id: str
    email: str
    display_name: Optional[str] = None
    locale: Optional[str] = None
    is_verified: Optional[bool] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        object.__setattr__(self, "metadata", _normalize_mapping(self.metadata))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EmailPasswordUserProfile":
        return cls(
            user_id=str(data.get("user_id") or data.get("id") or data.get("userId") or ""),
            email=_normalize_email(data.get("email")) or str(data.get("email") or ""),
            display_name=_normalize_string(data.get("display_name") or data.get("displayName")),
            locale=_normalize_locale(data.get("locale")),
            is_verified=_normalize_bool(data.get("is_verified") or data.get("isVerified")),
            metadata=_normalize_mapping(data.get("metadata")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PasswordResetResponse:
    email: str
    sent: bool = True
    locale: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        object.__setattr__(self, "metadata", _normalize_mapping(self.metadata))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PasswordResetResponse":
        return cls(
            email=_normalize_email(data.get("email")) or str(data.get("email") or ""),
            sent=_normalize_bool(data.get("sent")) if data.get("sent") is not None else True,
            locale=_normalize_locale(data.get("locale")),
            metadata=_normalize_mapping(data.get("metadata")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_request_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    data = dict(payload or {})
    if "email" in data:
        data["email"] = _normalize_email(data.get("email")) or data.get("email")
    if "locale" in data:
        data["locale"] = _normalize_locale(data.get("locale"))
    if "display_name" in data:
        data["display_name"] = _normalize_string(data.get("display_name"))
    if "displayName" in data:
        data["displayName"] = _normalize_string(data.get("displayName"))
    if "sent" in data:
        data["sent"] = _normalize_bool(data.get("sent"))
    return data


def normalize_response_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return normalize_request_payload(payload)

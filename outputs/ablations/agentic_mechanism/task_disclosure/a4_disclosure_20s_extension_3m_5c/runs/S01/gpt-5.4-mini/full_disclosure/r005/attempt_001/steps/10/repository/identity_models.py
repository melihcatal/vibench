import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Mapping, Optional


_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class IdentityModelError(ValueError):
    pass


def normalize_email(value: str) -> str:
    if not isinstance(value, str):
        raise IdentityModelError("email must be a string")
    normalized = value.strip().lower()
    if not normalized or not _EMAIL_RE.match(normalized):
        raise IdentityModelError("email must be a valid email address")
    return normalized


def normalize_locale(value: Optional[str]) -> str:
    if value is None:
        return "en"
    if not isinstance(value, str):
        raise IdentityModelError("locale must be a string")
    normalized = value.strip().replace("_", "-")
    return normalized or "en"


def normalize_trimmed_text(value: Optional[str], *, field_name: str, allow_empty: bool = False) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise IdentityModelError(f"{field_name} must be a string")
    normalized = " ".join(value.split())
    if not normalized and not allow_empty:
        raise IdentityModelError(f"{field_name} cannot be empty")
    return normalized


def normalize_metadata(value: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise IdentityModelError("metadata must be a mapping")
    return dict(value)


def _drop_none(data: Mapping[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}


@dataclass(frozen=True)
class EmailPasswordCredentials:
    email: str
    password: str
    locale: str = "en"

    def normalized(self) -> "EmailPasswordCredentials":
        return EmailPasswordCredentials(
            email=normalize_email(self.email),
            password=self.password,
            locale=normalize_locale(self.locale),
        )


@dataclass(frozen=True)
class RegisterUserRequest:
    email: str
    password: str
    user_metadata: Dict[str, Any] = field(default_factory=dict)
    locale: str = "en"

    def normalized(self) -> "RegisterUserRequest":
        return RegisterUserRequest(
            email=normalize_email(self.email),
            password=self.password,
            user_metadata=normalize_metadata(self.user_metadata),
            locale=normalize_locale(self.locale),
        )


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    realm: Optional[str] = None

    def normalized(self) -> "LoginRequest":
        return LoginRequest(
            email=normalize_email(self.email),
            password=self.password,
            audience=normalize_trimmed_text(self.audience, field_name="audience"),
            realm=normalize_trimmed_text(self.realm, field_name="realm"),
        )


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    connection: Optional[str] = None

    def normalized(self) -> "PasswordResetRequest":
        return PasswordResetRequest(
            email=normalize_email(self.email),
            connection=normalize_trimmed_text(self.connection, field_name="connection"),
        )


@dataclass(frozen=True)
class RefreshSessionRequest:
    refresh_token: str

    def normalized(self) -> "RefreshSessionRequest":
        token = normalize_trimmed_text(self.refresh_token, field_name="refresh_token")
        if token is None:
            raise IdentityModelError("refresh_token cannot be empty")
        return RefreshSessionRequest(refresh_token=token)


@dataclass(frozen=True)
class TokenResponse:
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    provider: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TokenResponse":
        data = dict(value)
        expires_in = data.get("expires_in")
        if expires_in is not None:
            try:
                expires_in = int(expires_in)
            except (TypeError, ValueError) as exc:
                raise IdentityModelError("expires_in must be an integer") from exc
        return cls(
            access_token=data.get("access_token"),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            token_type=data.get("token_type"),
            expires_in=expires_in,
            provider=data.get("provider"),
            raw=data,
        )

    def as_dict(self) -> Dict[str, Any]:
        return _drop_none(asdict(self))


@dataclass(frozen=True)
class OperationResponse:
    ok: bool = True
    message: Optional[str] = None
    provider: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any], *, default_ok: bool = True) -> "OperationResponse":
        data = dict(value)
        return cls(
            ok=bool(data.get("ok", default_ok)),
            message=data.get("message") or data.get("error_description") or data.get("error"),
            provider=data.get("provider"),
            raw=data,
        )

    def as_dict(self) -> Dict[str, Any]:
        return _drop_none(asdict(self))


__all__ = [
    "EmailPasswordCredentials",
    "IdentityModelError",
    "LoginRequest",
    "OperationResponse",
    "PasswordResetRequest",
    "RefreshSessionRequest",
    "RegisterUserRequest",
    "TokenResponse",
    "normalize_email",
    "normalize_locale",
    "normalize_metadata",
    "normalize_trimmed_text",
]
